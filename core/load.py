import os
import yaml
from models.agent import AgentItem, ToolItem
from core.cache import agents


def load_agents():
    global agents
    # 读取 agents 目录下的所有智能体信息
    path = './agents'
    agent_path = os.listdir(path)  # 获得文件夹中所有文件的名称列表
    for agent_name in agent_path:
        # 读取 yaml 配置文件信息
        with open("{0}/{1}/agent.yaml".format(path, agent_name), "r") as stream:
            agent_info = yaml.full_load(stream)
            # 工具列表
            tools = []
            for tool in agent_info["tools"]:
                tools.append(ToolItem(
                    name=tool["name"],
                    endpoint=tool["endpoint"],
                    classname=tool["classname"]
                ))
            agent_item = AgentItem(
                agent_id=agent_name,
                ver=agent_info["version"],
                name=agent_info["name"],
                author=agent_info["author"],
                desc=agent_info["desc"],
                avatar=agent_info["avatar"],
                temperature=float(agent_info["temperature"]),
                tools=tools
            )
            # 添加到智能体列表
            agents[agent_name] = agent_item
