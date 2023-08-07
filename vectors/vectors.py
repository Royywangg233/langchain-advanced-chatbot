import faiss
import pickle
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings


def load_index_and_vectors(index_path, vectors_path):
    index = faiss.read_index(index_path)
    with open(vectors_path, "rb") as f:
        vectors = pickle.load(f)
    vectors.index = index
    return vectors




