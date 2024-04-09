# import
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant

# create the open-source embedding function
embedding_function = OpenAIEmbeddings()

# load from disk
client = QdrantClient(host="localhost",port=6333)

db = Qdrant(
    client=client,
    embeddings = embedding_function,
    collection_name="all_documents"
    )

query = "how to upload a dataset"
# docs = db.similarity_search(query)
# found_docs = db.similarity_search_with_score(query , k=3)
# print(found_docs)
# for i, doc in enumerate(found_docs):
#     print(f"{i + 1}.", doc[1], "\n")
# print(docs[0].page_content)


found_docs = db.max_marginal_relevance_search(query, k=2, fetch_k=10)

for i, doc in enumerate(found_docs):
    print(f"{i + 1}.", doc.page_content, "\n")
