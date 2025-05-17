from openai import OpenAI

def get_ai_response(messages, secrets):
    client = OpenAI(api_key=secrets["API_KEY"], base_url=secrets["BASE_URL"])
    assistant_response = client.chat.completions.create(
        model=secrets["MODEL"],
        messages=messages
    )
    return assistant_response.choices[0].message.content
