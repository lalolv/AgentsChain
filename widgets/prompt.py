from fastapi import APIRouter
from core.cache import agents


router = APIRouter(prefix="/prompt")

# Prompt list
@router.get("/{agent_id}/list")
async def prompt_list(agent_id: str):
    global agents
    return agents[agent_id].prompts
