from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

embeddings = OpenAIEmbeddings()

# emb = embeddings.embed_query("Hello world")
# print(emb)

# Initialize the text splitter
text_splitter = CharacterTextSplitter(separator="\n", chunk_size=200, chunk_overlap=0)

# Initialize the OpenAI client
# chat = OpenAI()

# Load documents from a text file
loader = TextLoader("facts.txt")
docs = loader.load_and_split(
    text_splitter=text_splitter
)

# Print the loaded and split documents
for doc in docs:
    print(doc.page_content)
    print("-----")