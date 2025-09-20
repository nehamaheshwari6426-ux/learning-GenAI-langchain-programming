from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Chat LLM
chat = ChatOpenAI()

# Define the conversation memory
memory = ConversationBufferMemory(
    chat_memory=FileChatMessageHistory(file_path="messages/chat_history.json"),
    memory_key="messages", 
    return_messages=True)

# Define the prompt template with system message and human message
prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}"),
    ]
)

# Create the LLM chain with memory
chain = LLMChain(llm=chat, prompt=prompt, memory=memory)

while True:
    content = input(">> ")
    result = chain({"content": content})

    print(result["text"])
