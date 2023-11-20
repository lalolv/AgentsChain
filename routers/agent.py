from fastapi import APIRouter
from core.cache import agents
from fastapi.responses import FileResponse
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma


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


@router.post("/upload/{agent_id}")
async def upload_doc(agent_id: str):
    # Load the document, split it into chunks, embed each chunk and load it into the vector store.
    file_path = "agents/{0}/docs/state_of_the_union.txt".format(agent_id)
    raw_doc = TextLoader(file_path).load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_doc)
    Chroma.from_documents(
        documents=documents,
        persist_directory='vecdb',
        embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
        collection_name=agent_id,
        collection_metadata={'source': 'state_of_the_union.txt'}
    )

    return ""

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
