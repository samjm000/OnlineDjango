import pinecone
import os 
from haystack.document_stores import PineconeDocumentStore

def initiate_pinecone():
    print("Testing PInecone")
    ENV="eu-west1-gcp"
    API="0c463aad-1d8d-498d-a28a-177dcfd12711"
    document_store = PineconeDocumentStore(
        api_key=API,
        index='esmo', 
        environment=ENV, 
    )
    print(document_store.get_document_count())
    #pinecone.init(
    #    api_key="0c463aad-1d8d-498d-a28a-177dcfd12711", environment="eu-west1-gcp"
    #)
    #pinecone.create_index("quickstart", dimension=8, metric="euclidean", pod_type="p1")
    #print(pinecone.list_indexes())
    #print(pinecone.describe_index("esmo"))

    # Returns:
    # ['quickstart']
    #print(pinecone.list_indexes())
    #return document_store

initiate_pinecone()