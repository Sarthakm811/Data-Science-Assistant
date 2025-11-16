import os
from typing import Dict, Any, List
from kaggle.api.kaggle_api_extended import KaggleApi
from app.utils.config import settings


class KaggleTool:
    def __init__(self):
        self.api = KaggleApi()
        if settings.kaggle_username and settings.kaggle_key:
            os.environ["KAGGLE_USERNAME"] = settings.kaggle_username
            os.environ["KAGGLE_KEY"] = settings.kaggle_key
        self.api.authenticate()

    async def search_datasets(self, query: str, page: int = 1) -> List[Dict[str, Any]]:
        """Search Kaggle datasets"""
        datasets = self.api.dataset_list(search=query, page=page)
        return [
            {
                "id": f"{ds.ref}",
                "title": ds.title,
                "size": ds.size,
                "url": f"https://www.kaggle.com/datasets/{ds.ref}",
            }
            for ds in datasets[:10]
        ]

    async def get_dataset_info(self, dataset_id: str) -> Dict[str, Any]:
        """Get dataset metadata"""
        try:
            metadata = self.api.dataset_metadata(dataset_id)
            return {
                "id": dataset_id,
                "title": metadata.get("title", ""),
                "description": metadata.get("description", ""),
                "columns": metadata.get("columns", []),
            }
        except Exception as e:
            return {"id": dataset_id, "error": str(e)}

    async def get_dataset_summary(self, dataset_id: str) -> str:
        """Get dataset summary for prompt"""
        info = await self.get_dataset_info(dataset_id)
        return f"Dataset: {info.get('title', dataset_id)}\nDescription: {info.get('description', 'N/A')}"

    async def download_dataset(self, dataset_id: str, path: str = "/data"):
        """Download dataset to local path"""
        os.makedirs(path, exist_ok=True)
        self.api.dataset_download_files(dataset_id, path=path, unzip=True)
        return path
