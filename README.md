# Modeller 3D

Modeller turns a text description into a 3D landscape model. It combines a local retrieval-augmented generation (RAG) library of design references and Blender examples with AI-generated Blender Python, then runs Blender 5.2 in the background and presents the resulting GLB in a browser-based 3D viewer.

The project brings together a practical set of technologies: a web UI, a FastAPI job API, Azure-backed job and file storage, a local semantic-search index, AI-assisted code generation, and headless 3D rendering.

## What it does

- Accepts a short scene description through the web interface.
- Retrieves a relevant visual-design prompt and Blender Python example from separate local Chroma collections.
- Supplies those references to an AI model to help it generate Blender 5.2 scene-construction code.
- Executes the generated code with Blender 5.2 in background mode. If generation or execution fails, it can try the retrieved Blender example as a fallback.
- Appends the GLB export operation in the worker, using the exact output path for that job. Scene scripts do not hardcode an output filename.
- Checks that Blender created a GLB before uploading it to Azure Blob Storage.
- Tracks job status in Azure Cosmos DB and returns a short-lived, read-only URL for preview and download.
- Shows the model in an interactive browser viewer with rotate, zoom, and download controls.

## Screenshots

| Pine tree scene | Mountain scene | Rock cluster |
| --- | --- | --- |
| ![Generated low-poly pine tree landscape](<assets/Screenshot 2026-10-11 233856.png>) | ![Generated mountain scene](<assets/Screenshot 2026-10-11 234106.png>) | ![Generated rock cluster](<assets/Screenshot 2026-10-11 234439.png>) |

## How RAG helps create the 3D scene

RAG stands for **retrieval-augmented generation**. It lets the generation step use relevant material from a project-specific library instead of relying only on the user prompt and the model's general knowledge.

1. The project indexes the text files in `training_data/prompts/` and the Python files in `training_data/scripts/` into two separate Chroma collections: `landscape_prompts` and `landscape_scripts`.
2. For a new request, the worker performs semantic search against both collections and retrieves the closest visual reference and script example.
3. The worker sends the user's request and each reference in its own JSON field to the AI model. The visual reference can suggest details such as shape, color, and materials; the script reference can offer relevant Blender construction techniques.
4. The AI uses the references as guidance to write scene code for the specific request. It is not asked to return either reference file as the finished model.
5. Blender executes the code locally. The worker appends the export call and writes the resulting GLB to that job's own temporary output path.

In this way, RAG enhances model creation **indirectly**: it provides more relevant design and implementation context to the code-generation step. It does not itself generate geometry or render the model.

The current retrieval library is intentionally focused on landscapes. Its 30 prompt references and 30 script references cover mountains, rocks, vegetation, ground, water, and landscape structures. The same approach can be extended to other scenarios—such as architecture, product visualization, or interior scenes—by adding appropriate prompt and script examples, indexing them, and evaluating retrieval with queries relevant to those domains.

## Rendering and cost

The project does **not** call a third-party 3D rendering API. It creates scene code with Blender's Python API (`bpy`) and runs the installed Blender 5.2 executable locally in headless/background mode. This avoids a separate per-render charge from a hosted rendering service and gives the project direct control over scene construction and GLB export.

Other services are still used: an Azure OpenAI deployment generates Blender Python, Azure Cosmos DB stores job status, and Azure Blob Storage holds generated GLBs. These services may have usage-based costs. The sentence-transformer embedding model runs locally after it is available on the machine; its first use may download model files from Hugging Face.

## Project layout

```text
.
├── backend/
│   ├── main.py                 # FastAPI endpoints and prompt validation
│   ├── worker.py               # RAG, AI generation, Blender execution, upload
│   ├── azure_services.py       # Cosmos DB job tracking and Blob Storage
│   └── build_rag.py            # Index prompt and script training files
├── frontend/
│   ├── index.html              # Prompt form, job polling, GLB viewer/download
│   └── style.css
├── training_data/
│   ├── prompts/                # Design references, grouped by landscape category
│   └── scripts/                # Blender scene examples, grouped by category
├── tests/
│   ├── evaluate_retrieval.py
│   ├── retrieval_golden_set.json
│   └── script_retrieval_golden_set.json
├── assets/                     # README screenshots
└── rag_database/               # Persistent local Chroma database
```

## Setup

### Prerequisites

- Windows
- Python 3.11 (the development environment used for the project)
- Blender 5.2
- Azure OpenAI deployment with access to the Responses API
- Azure Storage account and Azure Cosmos DB account

### 1. Install Python dependencies

From the project root, create and activate a virtual environment, then install the packages used by the backend and RAG tooling:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn pydantic openai chromadb sentence-transformers azure-storage-blob azure-cosmos
```

If PowerShell does not allow activation scripts, use the virtual environment's interpreter directly (for example, `.venv\Scripts\python.exe -m pip install ...` and `.venv\Scripts\python.exe -m uvicorn ...`).

### 2. Configure environment variables

The backend reads credentials and configuration from environment variables. Set them in the PowerShell session that will run the API:

```powershell
$env:AZURE_OPENAI_ENDPOINT = "https://<your-resource>.openai.azure.com/openai/v1/"
$env:AZURE_OPENAI_API_KEY = "<your-api-key>"
$env:AZURE_OPENAI_DEPLOYMENT_NAME = "<your-model-deployment-name>"

$env:AZURE_STORAGE_CONNECTION_STRING = "<your-storage-connection-string>"
$env:AZURE_COSMOS_ENDPOINT = "https://<your-cosmos-account>.documents.azure.com:443/"
$env:AZURE_COSMOS_KEY = "<your-cosmos-key>"

$env:BLENDER_EXECUTABLE = "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
```

Use the actual endpoint, deployment name, account details, and Blender install path for your environment. Do not commit real credentials to the repository. `BLENDER_EXECUTABLE` can be omitted if Blender is available on `PATH`.

The Azure Storage connection string must include `AccountName` and `AccountKey`, which the application uses to create a read-only, one-hour SAS URL for the model viewer.

### 3. Build or refresh the local RAG index

Run from the project root after adding or changing training files:

```powershell
python -m backend.build_rag
```

The builder recursively reads both training directories and upserts their files into the `landscape_prompts` and `landscape_scripts` collections in `rag_database/`. The sentence-transformer model (`all-MiniLM-L6-v2`) is loaded locally and may be downloaded on its first use.

### 4. Start the API

```powershell
python -m uvicorn backend.main:app --reload
```

The API listens at `http://localhost:8000`. The browser UI currently sends requests to that local address.

### 5. Serve the frontend

In another PowerShell session, from the project root:

```powershell
python -m http.server 5500 --directory frontend
```

Open `http://localhost:5500` in a browser. The frontend talks to the local API; generated models and job state use the configured Azure services. If the browser cannot load a model from Blob Storage, check the storage account's Blob service CORS configuration for the frontend origin and `GET` access.

## Retrieval evaluation

The repository includes golden query sets: 30 user-style queries for prompt retrieval and 30 for script retrieval. Each query names the expected matching training file. The evaluation reports ranked filenames and distances, Hit@1, Hit@3, mean reciprocal rank (MRR), per-category results, and a demo-specific pass gate.

Run both evaluations from the project root:

```powershell
python tests/evaluate_retrieval.py
python tests/evaluate_retrieval.py --collection landscape_scripts --golden-set tests/script_retrieval_golden_set.json
```

The tested local index returned the expected result first for all 30 prompt queries and all 30 script queries: **Hit@1 = 100%, Hit@3 = 100%, and MRR = 1.000** for each collection. These results demonstrate that the current curated examples and queries work well together. They are not a guarantee for every possible request; adding training data or changing queries should be followed by rebuilding the index and running the evaluations again.

## API overview

- `POST /api/v1/generate/landscape-rag` — validates a prompt and queues a generation job.
- `GET /api/v1/jobs/{job_id}?user_id={user_id}` — retrieves the job's status and, on success, its model URL.

The generation endpoint accepts JSON with `prompt` and `user_id`. Prompts are limited to 500 characters and checked against a few basic instruction-injection patterns.

## Extending the project

To grow beyond landscape models, add relevant design references and Blender scene examples under `training_data/prompts/` and `training_data/scripts/`, organized by scenario or category. Rebuild the RAG index, add representative queries and expected filenames to the corresponding golden set, and run the retrieval evaluator. The current generator is landscape-oriented; broader content is best introduced alongside scenario-appropriate examples and evaluation queries.
