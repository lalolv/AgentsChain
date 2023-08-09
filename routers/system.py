from fastapi import APIRouter
import os


router = APIRouter(prefix="/sys")


@router.get("/info")
async def get_sys_info():
    openai_type = os.environ.get('OPENAI_API_TYPE')
    return {
        "status": "ok",
        "version": "0.0.1",
        "author": "Lalo",
        "openai_type": openai_type
    }
