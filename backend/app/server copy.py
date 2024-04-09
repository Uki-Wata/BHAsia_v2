#!/usr/bin/env python
from fastapi import FastAPI,APIRouter, Body
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
from starlette.middleware.cors import CORSMiddleware # 追加
from langserve import add_routes

app = FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)


class GenerateAWSServiceDescriptionRequest(BaseModel):
    input_text: str

@router.post("/aws_service_description")
async def generate_aws_service_description_endpoint(request: GenerateAWSServiceDescriptionRequest = Body(...)):
    input_text = request.input_text

    model = ChatOpenAI(model="gpt-4-turbo-preview", temperature=1.0, max_tokens=1000)
    description_output_parser = StrOutputParser()
    description_prompt = ChatPromptTemplate.from_template("""Must return markdown format.\nPlease tell me more about the AWS services you should use when building {input}.\nPlease express in a way that makes it easy to understand the relationship between the services that need to be linked.""")
    description_chain = description_prompt | model | description_output_parser
    description = description_chain.astream({"input": input_text})

    json_output_parser = JsonOutputParser()
    json_prompt = PromptTemplate(
        template="Answer the user query.Since you will want to create an architecture diagram in a later step, please make sure that you can understand the dependencies between each. Also, you only need to know the dependencies and service name.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": json_output_parser.get_format_instructions()}
    )
    json_chain = json_prompt | model | json_output_parser
    json_result = json_chain.astream({"query": description})

    return {
        "description": description,
        "json_result": json_result
    }

class GeneratePythonCodeRequest(BaseModel):
    input_text: str

@router.post("/generate_python_code")
async def generate_python_code_endpoint(request: GeneratePythonCodeRequest = Body(...)):
    input_text = request.input_text

    model = ChatOpenAI(model="gpt-4-turbo-preview", temperature=1.0, max_tokens=1000)
    output_parser = StrOutputParser()
    prompt = ChatPromptTemplate.from_template("""Express what you receive with {input} in python diagrams. There is no need to run it. Please do not return anything other than python code.""")
    prompt_with_input = prompt.partial(input=input_text)
    chain = (prompt_with_input | model | output_parser)
    result = chain.invoke({"input": input_text})

    return {"python_code": result}

class GenerateSecurityPrecautionsRequest(BaseModel):
    input_text: str

@router.post("/security_precautions")
async def generate_security_precautions_endpoint(request: GenerateSecurityPrecautionsRequest = Body(...)):
    input_text = request.input_text

    # Create the embedding function
    embedding_function = OpenAIEmbeddings()

    # Connect to the Qdrant client
    client = QdrantClient(host="localhost", port=6333)
    qdrant = Qdrant(
        client=client,
        embeddings=embedding_function,
        collection_name="test_documents"
    )

    # Create the retriever
    retriever = qdrant.as_retriever(search_type="mmr", verbose=True)
    contexts = retriever.get_relevant_documents(input_text)
    references = []
    for i, context in enumerate(contexts):
        references.append(context.metadata["source"])

    # Define the prompt template
    template = """Answer the question based only on the following context: {context}
    Question: What are the security matters that I need to keep in mind when using {aws_services}?
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Create the model
    model = ChatOpenAI()

    # Create the chain
    chain = (
        {"context": retriever, "aws_services": RunnablePassthrough()} | prompt | model | StrOutputParser()
    )
    result_md = chain.invoke(input_text)

    return {
        "result_md": result_md,
        "references": references
    }


# Assuming you have already defined the FastAPI app instance
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
