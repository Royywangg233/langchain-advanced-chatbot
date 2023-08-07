from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from contextlib import contextmanager
import time 

from chat.openai.openai import chatgpt
from chat.memory.memory import chat_memory
from chat.prompts.map_rerank.map_rerank_prompt import prompt
from config import TEMPRETURE, API_O, MODEL, MESSAGE
from chat.answer_processers.streaming import st_stream


@contextmanager
def timer():
    t1 = time.time()
    try:
        yield
    finally:
        t2 = time.time()
        global response_time
        response_time = round(t2 - t1, 1)


def start_chat(which_vectorstore, user_input, K, temperature=TEMPRETURE, api_o=API_O, model=MODEL, message=MESSAGE, prompt=prompt, debug=False):
    Conversation = load_qa_with_sources_chain(
        chatgpt(temperature, api_o, model, message), 
        prompt=prompt,
        chain_type="map_rerank",
        #memory=chat_memory(),
        verbose=True,
        return_intermediate_steps=True,
        rank_key="score",
        answer_key="answer",
        metadata_keys=['source']
    )

    with timer(): 
        similarity_search_results = which_vectorstore.similarity_search(user_input, k=K, fetch_k=K)
        pre_output = Conversation({"input_documents": similarity_search_results, "question": user_input}, return_only_outputs=True) #callbacks = [st_stream(MESSAGE)])
        print(pre_output)
    
    output = f"{pre_output['output_text']}\n\n**参考文档**:{pre_output['source']}\n\n**响应时间**:{response_time} 秒"
    output_without_reference = f"{pre_output['output_text']}\n\n**响应时间**:{response_time} 秒"
    score_value = [h['score'] for h in pre_output['intermediate_steps']]
    print(score_value)

    if debug == True:
        file_path_strings = [str(doc.metadata['source']) for doc in similarity_search_results]
        print(file_path_strings)
        return output, pre_output, file_path_strings, score_value
    
    else:
        return output, pre_output, score_value, output_without_reference
