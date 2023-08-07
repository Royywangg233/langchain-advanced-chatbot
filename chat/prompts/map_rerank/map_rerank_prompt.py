from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate

from chat.answer_processers.output_parser.regex import MY_RegexParser
from chat.prompts.map_rerank.example_selector import example_selector


output_parser = MY_RegexParser(
    regex=r"(.*?)\nScore: (.*)",
    output_keys=["answer", "score"]
)



prompt_template = """Use the following pieces of context to answer the question at the end. Your knowledge is only limited to the content below. If you know some parts of the answers, return it, but ALWAYS not to make up an answer, 不要编造答案. 
ALWAYS answer questions using bullet points. ALWAYS USE CHINESE to answer questions. You can retrieve any relevant text to answer my question, only if the documents has no relevant text to answer the question, just say: "从知识库无法回答此问题，请换一种问法。Score: 0"
ALWAYS include "Score:" value, instrcutions are below.

This is the format(You have to Always Follow this format):
"
[answer here]
Score: [score between 0 and 100]
"

How to determine the score:
- Higher is a better answer
- Always return a 'Score' value at the bottom of each question
- Better responds fully to the asked question, with sufficient level of detail
- If you do not know the answer based on the context, that should be a score of 0
- Don't be overconfident!


Begin!

Examples HERE:
---------
Question: {question}
Context: {context} 
---------
"""


PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context","question"]
)


suffix = """
[QUESTION]: {question}
=========
{context}
=========
[FINAL ANSWER]:
"""

prompt = FewShotPromptTemplate(
    example_selector=example_selector, 
    example_prompt=PROMPT, 
    suffix=suffix, 
    input_variables=["question", "context"],
    output_parser=output_parser,
)

