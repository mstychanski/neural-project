from openai import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from chat_openrouter import ChatOpenRouter



def get_ai_response(messages, secrets):
    client = OpenAI(api_key=secrets["API_KEY"], base_url=secrets["BASE_URL"])
    assistant_response = client.chat.completions.create(
        model=secrets["MODEL"],
        messages=messages
    )
    return assistant_response.choices[0].message.content


def answer_question(question, documents, model):


    template = """
        You are a helpful assistant. Answer the question based on the context provided. Answer in Polish by default.
        If the question is not answerable based on the context, say "I don't know".
        Context: {context}
        Question: {question}
        Answer:
    """

    context = "\n\n".join([doc["text"] for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"context": context, "question": question})
