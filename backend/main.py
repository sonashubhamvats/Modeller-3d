import logging
import re
import uuid

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

if __package__:
    from .azure_services import get_job_by_id, save_or_update_job
    from .worker import process_landscape_job
else:
    from azure_services import get_job_by_id, save_or_update_job
    from worker import process_landscape_job

logger = logging.getLogger("uvicorn.error")
app = FastAPI(title="3D Landscape Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_PROMPT_LENGTH = 500
INJECTION_PATTERNS = (
    re.compile(
        r"\b(?:ignore|disregard|forget|override|bypass)\b.{0,60}"
        r"\b(?:previous|prior|above|system|developer|safety|instructions?|rules?|guardrails?)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:reveal|show|print|repeat|output|expose|leak)\b.{0,60}"
        r"\b(?:system prompt|developer prompt|hidden instructions?|api keys?|secrets?)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:prompt injection|jailbreak|DAN mode)\b", re.IGNORECASE),
    re.compile(
        r"\b(?:act as|pretend to be|you are now)\b.{0,60}"
        r"\b(?:unrestricted|unfiltered|developer|system|different|another)\b",
        re.IGNORECASE,
    ),
)


class JobSubmission(BaseModel):
    prompt: str
    user_id: str


def validate_model_prompt(prompt: str) -> str:
    prompt = prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Please describe the 3D model to create.")
    if len(prompt) > MAX_PROMPT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Prompt must be {MAX_PROMPT_LENGTH} characters or fewer.",
        )
    if any(pattern.search(prompt) for pattern in INJECTION_PATTERNS):
        raise HTTPException(
            status_code=400,
            detail="The prompt contains instructions that are not allowed. Describe only the 3D model you want.",
        )
    return prompt


@app.post("/api/v1/generate/landscape-rag", status_code=202)
def submit_job(req: JobSubmission, background_tasks: BackgroundTasks):
    prompt = validate_model_prompt(req.prompt)
    job_id = f"job_{uuid.uuid4().hex[:8]}"

    save_or_update_job(job_id, req.user_id, prompt, "QUEUED", "Enqueued in worker")
    background_tasks.add_task(process_landscape_job, job_id, req.user_id, prompt)

    logger.info("Accepted model-generation job %s for user %s", job_id, req.user_id)
    return {
        "job_id": job_id,
        "status": "QUEUED",
        "poll_url": f"/api/v1/jobs/{job_id}?user_id={req.user_id}",
    }


@app.get("/api/v1/jobs/{job_id}")
def poll_job(job_id: str, user_id: str):
    job = get_job_by_id(job_id, user_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found in Azure Cosmos DB")
    return job
