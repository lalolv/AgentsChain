import os
from fastapi import APIRouter
from core.cache import agents
from fastapi.responses import FileResponse


router = APIRouter(prefix="/agent")


@router.get("/list")
# 获取机器人列表
async def get_agent_list():
    global agents
    # Get the database
    agent_list = []
    for item in agents.values():
        agent_list.append({
            "id": item.agent_id,
            "name": item.name,
            "desc": item.desc,
            "avatar": item.avatar,
            "tools": item.tools
        })

    return agent_list


@router.get("/detail/{agent_id}")
async def get_agent_detail(agent_id: str):
    global agents
    return agents[agent_id]


@router.get("/{agent_id}/avatar")
async def agent_avatar(agent_id: str):
    global agents
    agent_info = agents[agent_id]
    return FileResponse("agents/{0}/{1}".format(agent_id, agent_info.avatar))


# 获取文档资源链接
@router.get("/{agent_id}/docs/{name}")
async def doc_url(agent_id: str, name: str):
    file_path = "agents/{0}/docs/{1}".format(agent_id, name)
    if os.path.exists(file_path) is False:
        return ''
    
    return FileResponse(file_path)


# 获取代理的资源链接
@router.get("/{agent_id}/asset/{name}")
async def asset_url(agent_id: str, name: str):
    file_path = "agents/{0}/asset/{1}".format(agent_id, name)
    if os.path.exists(file_path) is False:
        return ''
    
    return FileResponse(file_path)
