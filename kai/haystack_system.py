import logging
import os
from haystack.document_stores import InMemoryDocumentStore
from haystack.utils import fetch_archive_from_http
from haystack.utils import print_answers
from pprint import pprint
from haystack.utils import fetch_archive_from_http
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
import asyncio
import time
from kai.pinecone_system import initiate_pinecone

# LOGGING
logging.basicConfig(
    format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING
)
logging.getLogger("haystack").setLevel(logging.INFO)

initiate_pinecone()

# DOC STORE
from haystack.document_stores import InMemoryDocumentStore

document_store = InMemoryDocumentStore(use_bm25=True)

# DATA
doc_dir = "data/esmo"


# write document objects into document store
import os
from haystack.pipelines.standard_pipelines import TextIndexingPipeline

files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
indexing_pipeline = TextIndexingPipeline(document_store)
indexing_pipeline.run_batch(file_paths=files_to_index)


# Retrieve from haystack.nodes import BM25Retriever
from haystack.nodes import BM25Retriever

retriever = BM25Retriever(document_store=document_store)

##INITIALIZE READER
from haystack.nodes import FARMReader

reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

##GET PIPELINE UP (RETRIEVER / READER)
from haystack.pipelines import ExtractiveQAPipeline

pipe = ExtractiveQAPipeline(reader, retriever)

prediction = ""


def predictionModel(question):
    if not question:
        return "You forgot to ask a question..."

    prediction = pipe.run(
        query=question, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}}
    )
    from haystack.utils import print_answers

    return print_answers(
        prediction, details="minimum"  ## Choose from `minimum`, `medium`, and `all`
    )
