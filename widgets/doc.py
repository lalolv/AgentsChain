import os
from fastapi import APIRouter, UploadFile
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma


router = APIRouter(prefix="/doc")


# Upload doc
@router.post("/upload/{agent_id}")
async def upload_doc(file: UploadFile, agent_id: str):
    # Upload file
    if file.filename is not None:
        # Save file
        save_file = os.path.join(
            "agents/{0}/docs/".format(agent_id), file.filename)
        f = open(save_file, 'wb')
        data = await file.read()
        f.write(data)
        f.close()
        # Load the document, split it into chunks, embed each chunk and load it into the vector store.
        raw_doc = TextLoader(save_file).load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        documents = text_splitter.split_documents(raw_doc)
        Chroma.from_documents(
            documents=documents,
            persist_directory='vecdb',
            embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
            collection_name=agent_id
        )

    return file.filename


# 测试
@router.get("/chroma/{agent_id}")
async def get_chroma(agent_id: str):
    db = Chroma(
        collection_name=agent_id,
        persist_directory='vecdb',
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )
    query = "What did the president say about Ketanji Brown Jackson"
    docs = db.similarity_search(query)
    return docs[0].page_content


# Doc list
@router.get("/{agent_id}/docs")
async def doc_list(agent_id: str):
    # 读取 agents 目录下的所有智能体信息
    path = './agents/{0}/docs'.format(agent_id)
    if os.path.exists(path) == False:
        return []
    # 按照创建时间排序
    file_list = sorted(
        os.listdir(path), 
        key=lambda x: os.path.getctime(os.path.join(path, x))
    )
    # 文件列表
    files = []
    for ff in file_list[:10]:
        # 文件大小
        file_size = os.path.getsize(os.path.join(path, ff))
        files.append({'name':ff, 'size':file_size})

    return files  # 获得文件夹中所有文件的名称列表
