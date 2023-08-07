import streamlit as st
import os
import re
import openai

from chat.answer_processers.image_processer import image_markdown
from chat.answer_processers.reference_processer import replace_with_http_link, reference_pattern
from chat.memory.memory import chat_memory
from config import TEMPRETURE, API_O, K, index_path, pkl_path, DEBUG
from chat.chain import start_chat
from vectors.vectors import load_index_and_vectors 
from chat.answer_processers.streaming import stream_print

os.environ["OPENAI_API_KEY"] = API_O
openai.proxy = {
            "http": "http://127.0.0.1:7890",
            "http": "https://127.0.0.1:7890"
        }


# Set Streamlit page configuration---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title='文档问答AI', layout='wide')

# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

if "input" not in st.session_state:
    st.session_state["input"] = ""

if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

if "previous_outputs" not in st.session_state:
    st.session_state["previous_outputs"] = ""

if 'entity_memory' not in st.session_state:
    st.session_state.entity_memory = chat_memory()

if 'something' not in st.session_state:
    st.session_state.something = ''


def submit():
    st.session_state.something = st.session_state.widget
    st.session_state.widget = ''

# Define function to start a new chat
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])        
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""

    #if 'entity_memory' not in st.session_state:
        #st.session_state.entity_memory = chat_memory()
    #st.session_state.entity_memory.save_context({"question": user_input}, {"output": "hi"})



# Set up sidebar with various options--------------------------------------------------------------------------------------------------------------------------------------------------------

with st.sidebar.expander("设置", expanded=False):
    MODEL = st.selectbox(label='Model', options=['gpt-3.5-turbo-16k-0613', 'gpt-4-0613'], index = 0)
    TEMPRETURE = st.slider('Tempreture',min_value=float(0),max_value=float(1), step=0.1, value = TEMPRETURE)
    VECTORSTORE = st.selectbox(label='向量库', options=['语雀'], index = 0, help = '开始提问前请确认当前向量库的名称')
    K = st.slider('查找参考文档数量',min_value=1,max_value=5, step=1, value = K, help = '参考文档数量越多，索引时间越久' )

#with st.sidebar.expander("其他", expanded=False):
    #DEBUG = st.selectbox(label='Debug', options=[True, False], index = 1, help = "会返回所有索引的参考文档的链接以及得分情况，用于查看回答问题的准确性。")


# Display ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.markdown(f'<h1 style="color:#1E2027;font-size:34px;font-family:Bangla MN;text-align: center;margin-left: -150px;">{"Langchain ChatBot "}</h1>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([0.31, 0.35, 0.34])

# Custom CSS styles--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
styl = f"""
  <style>
      .stTextInput {{
        position: fixed;
        bottom: 3rem;
        z-index: 1;
      }}
  </style>
  """
st.markdown(styl, unsafe_allow_html=True)


custom_css = """
<style>
input[type="text"] {
    background-color: #F0F0F0;  /* Set your desired background color */
    color: #1E2027;  /* Set your desired text color */
    background-color: #f2f2f2;
    font-family: monospace;
}

.stTextInput {{
        position: fixed;
        bottom: 3rem;
        z-index: 1;
      }}
      
</style>
"""

# Apply the custom CSS styles
st.markdown(custom_css, unsafe_allow_html=True)


# Allow to download as well---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def display_history():

    if st.session_state['generated']:
        #with st.expander("历史", expanded=True):
            for i in range(len(st.session_state['generated'])):
                st.markdown('<hr style="border: 0.8px solid grey; margin-top: 0.5em; margin-bottom: 0.9em;">', unsafe_allow_html=True)
                st.markdown(f"**问题:** {st.session_state['past'][i]}", unsafe_allow_html=True)
                st.markdown(st.session_state['generated'][i], unsafe_allow_html=True)
                #stream_print(st.session_state['generated'][i])



# get text ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_text():
    """
    Get the user input text.
    Returns:(str): The text entered by the user
    """
    input_text = st.text_input("请输入: ", st.session_state["input"], key="widget", on_change=submit, placeholder="我是听云AI, 有什么可以帮你....", label_visibility='hidden')      
    return st.session_state.something
    #return input_text


def create_new_chat_button():
    if st.sidebar.button("新建聊天", on_click=new_chat, type='primary'):
        del st.session_state.entity_memory


def display_stored_sessions():
    # Display stored conversation sessions in the sidebar
    for i, sublist in enumerate(st.session_state.stored_session):
        with st.sidebar.expander(label=f"谈话记录:{i}"):
            st.write(sublist)

    # Allow the user to clear all stored conversation sessions
    if st.session_state.stored_session:
        if st.sidebar.checkbox("清除记录"):
            del st.session_state.stored_session
            del st.session_state.entity_memory

            
# 向量库分类 --------------------------------------------------------------------------------------------------------------------------------------------------------
def process_vector_store(vectorstore, index_path, pkl_path):
    vectors = load_index_and_vectors(index_path, pkl_path)
    user_input = get_text()
    st.markdown('<hr style="border: 1.2px solid gray; margin-top: 0.5em; margin-bottom: 0.5em;">', unsafe_allow_html=True)
    st.markdown(f"**问题:** {user_input}", unsafe_allow_html=True)

    if user_input:
        if DEBUG == True:
            output, pre_output, file_path_strings, score_value = start_chat(vectors, user_input, K, debug=DEBUG)
            final_answer = re.sub(reference_pattern(), replace_with_http_link, output)
            image_have_markdown = image_markdown(pre_output["source"], final_answer)

            if image_have_markdown == False:
                #with st.expander('AI回答区', expanded=ANSWER):
                st.markdown(final_answer, unsafe_allow_html=True)
            
            with st.sidebar.expander("debug", expanded = True):
                for ii, score in zip(file_path_strings, score_value):
                    debug_reference = re.sub(reference_pattern(), replace_with_http_link, ii)
                    debug_reference_with_score = f"{debug_reference} (Score: {score})"
                    st.markdown(debug_reference_with_score, unsafe_allow_html=True)

        else:
            output, pre_output, score_value, output_without_reference = start_chat(vectors, user_input, K, debug=DEBUG)

            if all(value == "0" for value in score_value):
                stream_print(output_without_reference)
                
                st.session_state.past.append(user_input)
                st.session_state.generated.append(output_without_reference)
    
            
            else:
                final_answer = re.sub(reference_pattern(), replace_with_http_link, output)
                image_have_markdown = image_markdown(pre_output["source"], final_answer)

                if image_have_markdown == False:
                    #with st.expander('AI回答区', expanded=MESSAGE):
                    stream_print(final_answer)
                
                st.session_state.past.append(user_input)
                st.session_state.generated.append(final_answer)
                
                
def main():
    display_history()

    if VECTORSTORE == '我的向量库':
        process_vector_store('我的向量库', index_path, pkl_path)

    #elif VECTORSTORE == '帮助文档源文件':
        #process_vector_store('帮助文档源文件', index_path, pkl_path )
    
    display_stored_sessions()
    create_new_chat_button()
    

if __name__ == "__main__":
    main()
        
