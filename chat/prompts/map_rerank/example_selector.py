from langchain.prompts.example_selector import MaxMarginalRelevanceExampleSelector
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

import os
import openai

from config import API_0

os.environ["OPENAI_API_KEY"] = API_0


examples = [
  {
    "question": "悟空能不能获取AppKey?",
    "context": 
"""
在这里输入你的索引原文
Helpful Answer: 在这里输入你的自定义回答
Score: 90
"""
  },
  {
    "question": "APP如何限流？",
    "context": 
"""
在这里输入你的索引原文
Helpful Answer: 在这里输入你的自定义回答
Score: 50
"""
  },
  {
    "question": "APP如何限流？",
    "context": 
"""
在这里输入你的索引原文
Helpful Answer: 在这里输入你的自定义回答
Score: 50
"""
  },
  {
    "question": "what color are apples?",
    "context": 
"""
Pears are either red or orange
Helpful Answer: 从知识库无法回答此问题，请换一种问法。
Score: 0
"""
  },
  {
    "question": "xxx",
    "context": 
"""
xxxxx
xxxx
xxxx
Helpful Answer: xxxxx
Score: 90
"""
  }
]


example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    # This is the list of examples available to select from.
    examples,
    # This is the embedding class used to produce embeddings which are used to measure semantic similarity.
    OpenAIEmbeddings(),
    # This is the VectorStore class that is used to store the embeddings and do a similarity search over.
    FAISS,
    # This is the number of examples to produce.
    k=1
)



