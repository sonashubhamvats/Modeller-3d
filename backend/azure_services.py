# azure_services.py
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, ContentSettings, generate_blob_sas
from azure.cosmos import CosmosClient, PartitionKey, exceptions

# 1. Initialize Azure Blob Storage Client
blob_connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
storage_connection_settings = {
    key: value
    for setting in blob_connection_string.split(";")
    if "=" in setting
    for key, value in [setting.split("=", 1)]
}
CONTAINER_NAME = "models"

# 2. Initialize Azure Cosmos DB Client
cosmos_endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
cosmos_key = os.environ["AZURE_COSMOS_KEY"]
cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)

cosmos_db = cosmos_client.create_database_if_not_exists(id="ModellerDB")
jobs_container = cosmos_db.create_container_if_not_exists(
    id="jobs",
    partition_key=PartitionKey(path="/user_id")
)

def upload_glb_to_azure_blob(local_file_path: str, user_id: str, job_id: str) -> str:
    """Uploads a GLB and returns a short-lived, read-only URL for the viewer."""
    blob_name = f"{user_id}/{job_id}.glb"
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
    
    content_settings = ContentSettings(content_type="model/gltf-binary")
    
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True, content_settings=content_settings)

    account_name = storage_connection_settings.get("AccountName")
    account_key = storage_connection_settings.get("AccountKey")
    if not account_name or not account_key:
        raise ValueError(
            "AZURE_STORAGE_CONNECTION_STRING must include AccountName and AccountKey "
            "to create a read-only SAS URL for the model viewer."
        )

    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=CONTAINER_NAME,
        blob_name=blob_name,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    return f"{blob_client.url}?{sas_token}"

def save_or_update_job(job_id: str, user_id: str, prompt: str, status: str, stage: str, model_url: Optional[str] = None, error: Optional[str] = None):
    """Upserts job document state in Azure Cosmos DB."""
    item = {
        "id": job_id,
        "user_id": user_id,
        "prompt": prompt,
        "status": status,
        "stage": stage,
        "model_url": model_url,
        "error": error
    }
    jobs_container.upsert_item(item)

def get_job_by_id(job_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a job state document from Azure Cosmos DB by partition key."""
    try:
        response = jobs_container.read_item(item=job_id, partition_key=user_id)
        return response
    except exceptions.CosmosResourceNotFoundError:
        return None