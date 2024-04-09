import os
import glob
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant

def get_all_pdf_paths(directory):
    pdf_paths = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(dirpath, filename)
                pdf_paths.append(pdf_path)
    return pdf_paths

text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ".", ""],
    chunk_size=1000,
    chunk_overlap=50,
    length_function=len
)

embedding_function = OpenAIEmbeddings()
client = QdrantClient(host="localhost", port=6333)

# 単一のコレクション名
collection_name = "all_documents"

all_docs = []
for pdf_path in get_all_pdf_paths("./import_data"):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    docs = text_splitter.split_documents(documents)
    all_docs.extend(docs)

qdrant = Qdrant.from_documents(
    all_docs, embedding_function, collection_name=collection_name
)

query = "What is the best practice for AWS security?"
found_docs = qdrant.similarity_search(query)
print(found_docs[0].page_content)


