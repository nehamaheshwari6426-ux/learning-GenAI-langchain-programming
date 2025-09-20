import sqlite3
from pydantic.v1 import BaseModel
from typing import List
from langchain.tools import Tool

conn = sqlite3.connect('db.sqlite')

def list_tables():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return "\n".join(row[0] for row in tables if row[0] is not None) #[table[0] for table in tables]

def run_sqlite_query(query: str):
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        return f"The following error occurred: {str(e)}."
        # return f"The following error occurred: {str(e)}. Try reviewing the list of all available tables, table columns and extract schema for better understanding of data structure."

class RunQueryArgsSchema(BaseModel):
    query: str    

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query.",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema
)

def describe_tables(table_names):
    cursor = conn.cursor()
    try:
        tables = ', '.join([f"'{table}'" for table in table_names])
        rows = cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name in ({tables});")
        return "\n".join([row[0] for row in rows if row[0] is not None])
    except sqlite3.OperationalError as e:
        return f"The following error occurred: {str(e)}."
    
class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns the schema of the tables.",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)