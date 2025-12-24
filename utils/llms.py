from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0,
        convert_system_message_to_human=False
    )

llm = get_llm()



## Test Usage :
if __name__ == "__main__":
    response = llm.invoke("Hello, how are you?")
    print(response)
