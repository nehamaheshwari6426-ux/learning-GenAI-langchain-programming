from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--task",default="Return a list of numbers")
parser.add_argument("--language",default="Python")
args = parser.parse_args()

# Initialize the LLM
llm = OpenAI()

# --------------------------
# Templates
# --------------------------
# Define the prompt template
code_prompt = PromptTemplate(
    template="Write a very short {language} function that will {task}",
    input_variables=["language", "task"],
)

# Define a test prompt template to generate tests for the code
test_prompt = PromptTemplate(
    template = "Write a test for the following {language} code: {code}",
    input_variables = ["language", "code"]
)

# --------------------------
# Chains
# --------------------------
# Create the LLM chain
code_chain = LLMChain(llm=llm, prompt=code_prompt, output_key="code")

# Create a test chain 
test_chain = LLMChain(llm=llm, prompt=test_prompt, output_key="test")

final_chain = SequentialChain(
    chains=[code_chain, test_chain],
    input_variables=["language", "task"],
    output_variables=["code", "test"],
    # verbose=True
)

# Run the chain with the provided arguments
final_chain_result = final_chain({"language": args.language, "task": args.task})

print("Final Chain Result:")
print(final_chain_result.get("code"))

print("Test for the code:")
print(final_chain_result.get("test"))