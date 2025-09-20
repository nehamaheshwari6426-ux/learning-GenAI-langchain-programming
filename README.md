# learning-GenAI-langchain-programming
Telstra GenAI: LangChain Programming


## Initial Set-up
`
# Install Python 3.12
brew install python@3.12

# Make a new 3.12 virtualenv in your project
/opt/homebrew/bin/python3.12 -m venv .venv312
source .venv312/bin/activate

# Upgrade packaging tools and install
python -m pip install --upgrade pip setuptools wheel
<!-- python -m pip install tiktoken -->

# Install pipenv uisng pip
pip install pipenv

# Install dependencies from the Pipfile
pipenv install

# run the code to create and enter a new environment
pipenv shell 

# to exit
deactivate
`

# Restart the virtual environment
`
source .venv312/bin/activate
pipenv install
`
