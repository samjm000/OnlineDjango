import logging
import os
import time
from haystack.utils import print_answers
from pprint import pprint


logging.basicConfig(
    format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING
)
logging.getLogger("haystack").setLevel(logging.INFO)


## IMPORT DOCUMENT STORE
from haystack.document_stores import InMemoryDocumentStore

document_store = InMemoryDocumentStore(use_bm25=True)

## PREPARE DOCUMENTS
from haystack.utils import fetch_archive_from_http


doc_dir = "data/esmo"
# doc_dir = "data/build_your_first_question_answering_system"
# fetch_archive_from_http(
#    url="https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt1.zip",
output_dir = doc_dir
# )


##CONVERT TO HAYSTACK DOCUMENTS
import os
from haystack.pipelines.standard_pipelines import TextIndexingPipeline

files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
indexing_pipeline = TextIndexingPipeline(document_store)
indexing_pipeline.run_batch(file_paths=files_to_index)

##INITIALIZE RETRIEVER
from haystack.nodes import BM25Retriever

retriever = BM25Retriever(document_store=document_store)

##INITIALIZE READER
from haystack.nodes import FARMReader

reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

##GET PIPELINE UP
from haystack.pipelines import ExtractiveQAPipeline
pipe = ExtractiveQAPipeline(reader, retriever)


def predictionModel(question):
    if question:
        prediction = pipe.run(
            query=question, params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 1}}
        )
    # end_result = pprint(prediction)
    # time.sleep(3)
    if not prediction:
        return ""
    return prediction
