# ================================================= 
# How do we get back responses from LLMs in strictly json format
# OpenAI chat
# ================================================= 

from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
    {"role": "user", "content": "Who won the world series in 2020?"}
  ]
)
print(response.choices[0].message.content)

# ================================================= 
# https://python.langchain.com/docs/modules/model_io/output_parsers/quick_start
# using langchain
# ================================================= 

from langchain.output_parsers.json import SimpleJsonOutputParser

json_prompt = PromptTemplate.from_template(
    "Return a JSON object with an `answer` key that answers the following question: {question}"
)
json_parser = SimpleJsonOutputParser()
json_chain = json_prompt | model | json_parser

list(json_chain.stream({"question": "Who invented the microscope?"}))

# ================================================= 
# https://python.langchain.com/docs/modules/model_io/output_parsers/types/json
# using langchain
# ================================================= 
from typing import List

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

model = ChatOpenAI(temperature=0)

# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

# And a query intented to prompt a language model to populate the data structure.
joke_query = "Tell me a joke."

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

chain.invoke({"query": joke_query})

# output: 
# {'setup': "Why don't scientists trust atoms?",
#  'punchline': 'Because they make up everything!'}

# Refer to this as well 
https://www.gettingstarted.ai/how-to-langchain-output-parsers-convert-text-to-objects/

