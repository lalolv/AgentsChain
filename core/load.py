import os
import yaml
from models.agent import AgentItem, ToolItem, PromptItem
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

            # 预设提示词列表
            prompts = []
            for prompt in agent_info["prompts"]:
                prompts.append(PromptItem(
                    name=prompt["name"],
                    prompt=prompt["prompt"],
                ))

            # 添加到智能体列表
            agent_item = AgentItem(
                agent_id=agent_name,
                agent_type=agent_info["type"],
                ver=agent_info["version"],
                name=agent_info["name"],
                author=agent_info["author"],
                desc=agent_info["desc"],
                avatar=agent_info["avatar"],
                temperature=float(agent_info["temperature"]),
                tools=agent_info["tools"],
                prompts=prompts
            )
            
            # 添加到智能体列表
            agents[agent_name] = agent_item
