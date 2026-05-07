from fastapi import APIRouter
from services.logger import get_metrics

router = APIRouter()

@router.get("/metrics")
async def metrics():
    return await get_metrics()