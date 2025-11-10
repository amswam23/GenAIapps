from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Optional Hugging Face embeddings
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    HF_AVAILABLE = True
except ModuleNotFoundError:
    HF_AVAILABLE = False


def get_embeddings(embedding_model="OpenAI"):
    if embedding_model.lower() == "openai":
        return OpenAIEmbeddings(model="text-embedding-3-large")
    elif embedding_model.lower() == "huggingface" and HF_AVAILABLE:
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    else:
        return OpenAIEmbeddings(model="text-embedding-3-large")


def build_vectorstore(text, embedding_model="OpenAI"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    embeddings = get_embeddings(embedding_model)
    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore


def retrieve_relevant_chunks(vectorstore, query, k=4):
    docs = vectorstore.similarity_search(query, k=k)
    return [getattr(doc, "page_content", str(doc)) for doc in docs]
