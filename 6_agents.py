from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.reports import write_report_tool

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
        MessagesPlaceholder(variable_name="chat_history"),

        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
tools = [run_query_tool, describe_tables_tool, write_report_tool]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# agent_executor.run("How many users have provided shipping addresses?")
# agent_executor.run("Summarise the top 5 most popular products. Write the results to a report file.")
agent_executor.run("How many orders are there? Write the result to an html report.")

agent_executor.run("Repeat the exact same process for users.")