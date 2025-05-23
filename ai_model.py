from openai import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from chat_openrouter import ChatOpenRouter



def get_ai_response(messages, secrets, documents=None, model=None):
    """
    Jeśli przekazano documents i model, użyj answer_question.
    W przeciwnym razie fallback do klasycznego OpenAI.
    """
    if documents is not None and model is not None:
        question = messages[-1]["content"] if messages else ""
        return answer_question(question, documents, model)
    else:
        client = OpenAI(api_key=secrets["API_KEY"], base_url=secrets["BASE_URL"])
        assistant_response = client.chat.completions.create(
            model=secrets["MODEL"],
            messages=messages
        )
        return assistant_response.choices[0].message.content


def answer_question(question, documents, model, template):


    context = "\n\n".join([doc["text"] for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"context": context, "question": question})
