from fastapi import APIRouter, HTTPException
from typing import List
from app.tools.kaggle_tool import KaggleTool

router = APIRouter()
kaggle_tool = KaggleTool()

@router.get("/datasets/search")
async def search_datasets(q: str, page: int = 1):
    """Search Kaggle datasets"""
    try:
        results = await kaggle_tool.search_datasets(q, page)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/datasets/{dataset_id}")
async def get_dataset(dataset_id: str):
    """Get dataset details"""
    try:
        info = await kaggle_tool.get_dataset_info(dataset_id)
        return info
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
