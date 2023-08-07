from langchain.chat_models import ChatOpenAI

from chat.answer_processers.streaming import st_stream
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler 


def chatgpt(TEMPRETURE, API_O, MODEL, MESSAGE):
    return ChatOpenAI(temperature=TEMPRETURE,
                      openai_api_key=API_O, 
                      model_name=MODEL, 
                      streaming =True, 
                      #callbacks=[st_stream(MESSAGE)]
            )