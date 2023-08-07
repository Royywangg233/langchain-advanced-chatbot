print("开始")
import os
from pathlib import Path
import faiss
import pickle
import openai
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter 

from config import API_O, load_file_path,index_path,pkl_path


os.environ["OPENAI_API_KEY"] = API_O
openai.proxy = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890"
        }


def split_doc(chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter


def load_markdown(path = load_file_path, text_splitter = split_doc(chunk_size=1300, chunk_overlap=300)):
    ps = list(Path(load_file_path).glob("**/*.md"))
    data = []
    sources = []
    for p in ps:
        with open(p, encoding="utf-8") as f:
            data.append(f.read())
        sources.append(p)

    docs = []
    metadatas = []
    for i, d in enumerate(data):
        splits = text_splitter.split_text(d)
        docs.extend(splits)
        metadatas.extend([{"source": sources[i]}] * len(splits))
    
    return docs, metadatas


# 持久化数据 
docs, metadatas = load_markdown()
store = FAISS.from_texts(docs, OpenAIEmbeddings(), metadatas=metadatas)
faiss.write_index(store.index, index_path)
store.index = None
with open(pkl_path, "wb") as f:
    pickle.dump(store, f)
    
print("完成向量库构建")



 
        
