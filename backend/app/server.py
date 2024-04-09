import json
from fastapi import APIRouter, FastAPI
from langchain.chat_models import ChatAnthropic, ChatOpenAI
from fastapi import FastAPI,APIRouter, Body
from numpy import add
from pydantic import BaseModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from starlette.middleware.cors import CORSMiddleware
from langserve import add_routes
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_experimental.tools import PythonREPLTool
from sympy import im, python


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)




model = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
description_output_parser = StrOutputParser()
description_prompt = ChatPromptTemplate.from_template("""Must return markdown format.\nPlease tell me more about the AWS services you should use when building {input}.\nPlease express in a way that makes it easy to understand the relationship between the services that need to be linked.""")
description_chain = description_prompt | model | description_output_parser


json_output_parser = JsonOutputParser()
json_template = """Create a JSON structure that represents AWS service dependencies with services as an array of objects, each with name, description, and dependencies, where dependencies includes dependent name, description, and optional typeSince you will want to create an architecture diagram in a later step, please make sure that you can understand the dependencies between each. Also, you only need to know the dependencies and service name.{format_instructions}{query}."""
json_prompt = PromptTemplate(
    template=json_template,
    input_variables=["query"],
    partial_variables={"format_instructions": json_output_parser.get_format_instructions()}
)
json_chain = json_prompt | model | json_output_parser




add_routes(app, description_chain, path="/description")
add_routes(app, json_chain, path="/json")

# Create the embedding function
embedding_function = OpenAIEmbeddings()

# Connect to the Qdrant client
qdrant_client = QdrantClient(host="localhost", port=6333)
qdrant = Qdrant(
    client=qdrant_client,
    embeddings=embedding_function,
    collection_name="all_documents"
)

# Create the retriever
retriever = qdrant.as_retriever(search_type="mmr",k=10, verbose=True)

# Define the prompt template
aws_rag_template = """Based on the information provided in {context}, please provide a detailed analysis of the key security considerations to keep in mind when using {aws_services}. Your response should cite the relevant sections directly from the context to support each security measure listed. Please structure your response as follows: Security Considerations
Security Considerations List in bulleted detail all major concerns, potential risks/threats, and recommended safeguards related to the use of {aws_services} extracted from the context.
Rationale For each security measure, cite the supporting rationale in context. Relevant passages should be indicated in quotation marks, followed by the document information.
Example: "Rationale passage cited from context" Source: [document title] (page number)
Use this format to provide a quote from the context and its source for each security consideration listed.
"""
aws_rag_prompt = ChatPromptTemplate.from_template(aws_rag_template)

# Create the chain
aws_rag_chain = (
    {"context": retriever, "aws_services": RunnablePassthrough()} | aws_rag_prompt | model | StrOutputParser()
)

add_routes(app, aws_rag_chain, path="/rag")

from langchain.load import dumps, loads

generate_queries_template = """You are a helpful assistant that generates multiple search queries based on a single input query. \n
Generate multiple search queries related to: {question} \n
Output (4 queries):"""
generate_queries_prompt = ChatPromptTemplate.from_template(generate_queries_template)

def reciprocal_rank_fusion(results: list[list], k=60):
    """Rerank docs (Reciprocal Rank Fusion)

    Args:
        results (list[list]): retrieved documents
        k (int, optional): parameter k for RRF. Defaults to 60.

    Returns:
        ranked_results: list of documents reranked by RRF
    """

    fused_scores = {}
    for docs in results:
        # Assumes the docs are returned in sorted order of relevance
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            fused_scores[doc_str] += 1 / (rank + k)

    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]

    # return only documents
    return [x[0] for x in reranked_results[:8]]


generate_queries_chain = (
    {"question": RunnablePassthrough()}| generate_queries_prompt | model | StrOutputParser() | (lambda x: x.split("\n"))
)

fusion_rag_template = """Answer the following question based on this context:

{context}

Question: {question}
"""

fusion_rag_prompt = ChatPromptTemplate.from_template(fusion_rag_template)


retrieve_chain = (
   {"original_query": RunnablePassthrough()}
   | generate_queries_chain
   | retriever.map()
   | reciprocal_rank_fusion
)

fusion_rag_chain = (
   {
       "context": retrieve_chain,
       "question": RunnablePassthrough(),
   }
   | fusion_rag_prompt
   | model
   | StrOutputParser()
)

add_routes(app, fusion_rag_chain, path="/fusion-rag",input_type=str)


python_code_generate_output_parser = StrOutputParser()
python_code_generate_prompt = ChatPromptTemplate.from_template("""Express what you receive with {input} in python diagrams. Be sure to include filename in the Diagram class.There is no need to run it. Please do not return anything other than python code.""")

python_code_generate_chain = python_code_generate_prompt | model | python_code_generate_output_parser

add_routes(app, python_code_generate_chain, path="/python-code-generate")



python_tool = [PythonREPLTool()]
python_tool_instructions = """You are an agent designed to write and execute python code to answer questions. You have access to a python REPL, which you can use to execute python code. If you get an error, debug your code and try again. Only use the output of your code to answer the question. You might know the answer without running any code, but you should still run the code to get the answer. If it does not seem like you can write code to answer the question, just return "I don't know" as the answer. """
base_prompt = hub.pull("hwchase17/openai-functions-agent")
python_prompt = base_prompt.partial(instructions=python_tool_instructions)
python_agent = create_openai_functions_agent(ChatOpenAI(model="gpt-3.5-turbo",temperature=0), python_tool, python_prompt)
python_agent_input_text = f"""
Run the code below with python diagrams and save the output image and move to the ./backend/app/images/ path.
```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("My Sample Architecture", filename="sample_architecture"):
    with Cluster("VPC"):
        with Cluster("Public Subnet"):
            elb = ELB("Load Balancer")

        with Cluster("Private Subnet"):
            ec2_1 = EC2("Web Server 1")
            ec2_2 = EC2("Web Server 2")
            rds = RDS("Database")

    elb >> ec2_1
    elb >> ec2_2
    ec2_1 >> rds
    ec2_2 >> rds
```
"""
pythonagent_executor = AgentExecutor(agent=python_agent, tools=python_tool, verbose=True)
class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: str


add_routes(app, pythonagent_executor.with_types(input_type=Input, output_type=Output), path="/pythonagent")



from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app.mount("/images", StaticFiles(directory="app/images"), name="images")
@app.get("/get-image/{image_name}")
async def get_image(image_name: str):
    image_path = f"app/images/{image_name}"
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        # 画像が見つからない場合の処理
        return {"message": "Image not found"}
