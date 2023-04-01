import pinecone


def initiate_pinecone():
    print("Testing PInecone")
    pinecone.init(
        api_key="098671e2-0c18-4de5-8d44-1e00683b1671", environment="YOUR_ENVIRONMENT"
    )
    pinecone.create_index("quickstart", dimension=8, metric="euclidean", pod_type="p1")
    pinecone.list_indexes()

    # Returns:
    # ['quickstart']
    print(pinecone.list_indexes())


initiate_pinecone()
