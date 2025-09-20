from langchain.vectorstores import Chroma
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# import langchain
# langchain.debug = True

# Load environment variables from a .env file
load_dotenv()

# Initialize the OpenAI client and embeddings
chat = OpenAI()
embeddings = OpenAIEmbeddings()

# Initialize the vector store using Chroma
db = Chroma(
    persist_directory="emb",
    embedding_function=embeddings,
)
# Create a retriever from the vector store
retriever = db.as_retriever()

# Create a RetrievalQA chain
chain = RetrievalQA.from_chain_type(
    llm=chat,
    retriever=retriever,
    chain_type="stuff",
)

result = chain.run("What is an interesting fact about Earth?")

print(result)
print("\n")