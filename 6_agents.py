from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool

# Load environment variables from a .env file
load_dotenv()

chat = ChatOpenAI()

tables = list_tables()

prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI that has access to SQLite database.\n"
            f"The database tables are:\n {tables}\n"
            "Do not make assumptions about what tables exist "
            "or what columns they contain. Instead, use the 'describe_tables' function."
            # f"You are an helpful agent that have access to a SQLite database. The available tables in the database are:\n {tables}"
        )),

        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

tools = [run_query_tool, describe_tables_tool]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

agent_executor.run("How many users have provided shipping addresses?")