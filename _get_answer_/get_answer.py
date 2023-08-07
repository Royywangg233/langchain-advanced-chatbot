import streamlit as st
import os
import re
import openai

from chat.answer_processers.image_processer import image_markdown
from chat.answer_processers.reference_processer import replace_with_http_link, reference_pattern
from chat.memory.memory import chat_memory
from config import TEMPRETURE, API_O, K
from chat.chain import start_chat
from vectors.vectors import load_index_and_vectors 
from config import index_path, pkl_path


os.environ["OPENAI_API_KEY"] = API_O
openai.proxy = {
            "http": "http://127.0.0.1:7890",
            "http": "https://127.0.0.1:7890"
        }


def get_answer(user_input):
    DEBUG = False
    IMAGE = False
    ANSWER = False
    vectors = load_index_and_vectors(index_path, pkl_path)
    if user_input:
        if DEBUG == True:
            output, pre_output, file_path_strings, score_value = start_chat(vectors, user_input, K, debug=DEBUG)
            final_answer = re.sub(reference_pattern(), replace_with_http_link, output)
            
            with st.sidebar.expander("debug", expanded = True):
                for ii, score in zip(file_path_strings, score_value):
                    debug_reference = re.sub(reference_pattern(), replace_with_http_link, ii)
                    debug_reference_with_score = f"{debug_reference} (Score: {score})"
                    print(debug_reference_with_score)

        else:
            output, pre_output, score_value, output_without_reference = start_chat(vectors, user_input, K, debug=DEBUG)
            if all(value == "0" for value in score_value):
                return output_without_reference
            
            else:
                final_answer = re.sub(reference_pattern(), replace_with_http_link, output)
                return final_answer
# 无streaming 无memory
answer = get_answer(user_input = input())       
print(answer)