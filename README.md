# AppChainAI 接口服务

## 如何运行

### 开发环境

```shell
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### 生产环境

```shell
gunicorn -b :8080 -w 4 main:app -k uvicorn.workers.UvicornWorker
```

## 如何部署

```shell
gcloud run deploy dox-api --source .
```

The requirements.txt file is generated by the poetry tool:

```shell
poetry export --without-hashes --format=requirements.txt > requirements.txt
```
