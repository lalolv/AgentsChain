<div align="center" width="100px">
 <picture>
   <img width="100" src="./public/logo.png">
 </picture>
</div>

<div align="center">

<h1>AgentsChain 智能体</h1>

简体中文 | [English](./README_en.md)

基于 LangChain 框架的开源智能体 Agent 项目

可以定制创建自己的智能体 Agent

自由创建工具的功能性扩展

[官网](https://appchain.ai) / [Youtube](https://www.youtube.com/channel/UCjuEShkFKxJQaNc8i6xyPTA) / [Twitter](https://twitter.com/AppChainAI)

</div>

![cover](./public/banner.png)

# AgentsChain 智能体

## Overview 概述

代理是一个用于构建自治语言代理的开源库/框架。该库经过精心设计，以支持重要功能，包括长期短期记忆、工具使用、Web 导航、多智能体通信以及包括人代理交互和符号控制在内的全新功能。使用代理，只需用自然语言填写配置文件，并在终端、Gradio 接口或后端服务中部署语言代理，即可自定义语言代理或多代理系统。

## 📢 Updates

[x] 2023.10.26 发布第一个 Demo

## 💡 Highlights 亮点

- **Long-short Term Memory**: Language agents in the

## 🛠️ 如何运行

### 开发环境

使用 uvicorn

```shell
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

使用 JinaAI 的 langchain-serve

```shell
lc-serve deploy local --app main:app
```

### 生产环境

```shell
gunicorn -b :8080 -w 4 main:app -k uvicorn.workers.UvicornWorker
```

## 📦 如何部署

```shell
gcloud run deploy dox-api --source .
```

使用 JinaAI 的 jcloud 云部署

```shell
lc-serve deploy jcloud --app main:app --secrets .env
```

The requirements.txt file is generated by the poetry tool:

```shell
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

Use pipreqs

```shell
pipreqs --force ./
```
