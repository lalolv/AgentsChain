from fastapi import APIRouter
import os
import importlib


router = APIRouter(prefix="/sys")


@router.get("/info")
async def get_sys_info():
    openai_type = os.environ.get('OPENAI_API_TYPE')
    return {
        "status": "ok",
        "version": "0.1.0",
        "author": "Lalo",
        "openai_type": openai_type
    }


@router.get("/test")
async def test():
    mod = importlib.import_module("agents.search.test")
    ret = ""
    if hasattr(mod, "ToolRun"):    
        ToolClass = getattr(mod, 'ToolRun')
        tool = ToolClass()
        ret = tool.run("Hey")
    return ret
