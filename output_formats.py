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
