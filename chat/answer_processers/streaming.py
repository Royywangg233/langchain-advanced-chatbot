import streamlit as st
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import re


class StreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, container, initial_text="", buffer_size=1000):
        self.container = container
        self.text = initial_text
        self.buffer = []
        self.buffer_size = buffer_size

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.buffer.append(token)
        # 如果缓冲区的大小超过了最大值，删除最旧的令牌
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)
           
        # 将缓冲区中的令牌合并为一个字符串
        buffer_str = "".join(self.buffer)
        # 检查这个字符串是否包含"参考文档"
        if "从知识库无法回答此问题，请换一种问法。" in buffer_str:
            buffer_str = buffer_str.replace("从知识库无法回答此问题，请换一种问法。", "")
        #self.text += token
        self.container.markdown(buffer_str, unsafe_allow_html=True)


def st_stream(MESSAGE):
    with st.expander("思考中...", expanded=MESSAGE):
        #st.markdown(f'<h1 style="color:#1E2027;font-size:20px;font-family:Bangla MN;">{"ChatGPT "}</h1>', unsafe_allow_html=True)
        chat_box = st.empty()
        stream_handler = StreamHandler(chat_box)
    
        return stream_handler   


import time
def stream_print(text):
    container = st.empty()  # 创建一个空的容器
    output = ""
    for char in text:
        if char == "\n":
            output += "\n"
        else:
            output += char
        container.markdown(f"{output}", unsafe_allow_html=True)
        time.sleep(0.008)