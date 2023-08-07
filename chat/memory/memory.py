from langchain.memory import ConversationStringBufferMemory
from langchain.memory import ConversationTokenBufferMemory, ConversationBufferMemory
from langchain.memory import CombinedMemory, ChatMessageHistory
from langchain.chat_models import ChatOpenAI



def chat_memory():
    buffer = ConversationBufferMemory(memory_key="chat_history",input_key="question",output_key='output_text')
    #token_buffer = ConversationTokenBufferMemory(llm=ChatOpenAI(),chat_memory=ChatMessageHistory(messages=[]),input_key="question", max_token_limit=2000,output_key='output_text',return_messages=True,)
    #token_buffer.save_context({"question": "hhhh一加一等于几？"}, {"output_text": "一加一等于二"})
    #string_buffer = ConversationStringBufferMemory(input_key="question",memory_key="chat_history",output_key='output_text')
    # Combined
    #memory = CombinedMemory(memories=[token_buffer, string_buffer])

    return buffer