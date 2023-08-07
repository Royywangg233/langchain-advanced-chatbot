from langchain import PromptTemplate

# refine chain type ---------------------------------------------------------------------------------------------------------------------------------
def refine_prompt():
    refine_prompt_template = (
        "\n Reply in Chinese\n"
        "We have the opportunity to refine the existing answer"
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{context_str}\n"
        "------------\n"
        "Given the new context, refine the original answer to better "
        "answer the question. "
        "如果跟答案无关，停止思考"
        "The original question is as follows: {question}\n"
        "你是一所科技公司的顾问人员，用中文回答前来咨询的人的问题，你具备常识。你拥有编程的能力，你拥有前端开发的能力，你拥有后端开发的能力。你只回答本地文档里所拥有的内容。如果你不会，请说 “我不知道”，一定不要试图编造。\n" 
        "Give your answers using bullet points.If you not sure about the answer just say that I need more information, and reassure what the user wants to ask.If you don't know the answer, just say you don't know, do not make up the answer, and provide fake response.You don't need to summerize the text, just stuff all you got. ALWAYS return a 'SOURCES' part at the bottom of your answer if you referred anything, for example “\n**参考文档**：xxxxxxxx.md”"
    "这个是你告诉我的话:{existing_answer}\n"

    )
    refine_prompt = PromptTemplate(
        input_variables=["question", "context_str", "existing_answer"],
        template=refine_prompt_template,
    )

    return refine_prompt



def initial_qa_prompt():
    initial_qa_template = (
        "Context information is below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "如果跟文本一点也不匹配，停止思考 返回:'我不知道'"
        "If you not sure about the answer just say that I need more information, and reassure what the user wants to ask.If you don't know the answer, just say you don't know, do not make up the answer, and provide fake response."
        "\n这是跟之前谈话内容相关的区域：\n\n{chat_history}"
        "问题:{question}\nYour answer should be in Chinese.\n"
    )

    initial_qa_prompt = PromptTemplate(
        input_variables=["context_str", "question", "chat_history"], template=initial_qa_template
    )

    return initial_qa_prompt

