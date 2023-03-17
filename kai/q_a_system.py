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

from haystack.utils import launch_es
#launch_es() -> Do manually / add to docker in production

#LOGGING
logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)


from haystack.document_stores import ElasticsearchDocumentStore
# Get the host where Elasticsearch is running, default to localhost (will need new server added)
host = os.environ.get("ELASTICSEARCH_HOST", "localhost")

document_store = ElasticsearchDocumentStore(
    host=host,
    username="",
    password="",
    index="document"
)

from haystack import Pipeline
from haystack.nodes import TextConverter, PreProcessor

indexing_pipeline = Pipeline()
text_converter = TextConverter()
preprocessor = PreProcessor(
    clean_whitespace=True,
    clean_header_footer=True,
    clean_empty_lines=True,
    split_by="word",
    split_length=200,
    split_overlap=20,
    split_respect_sentence_boundary=True,
)

#DATA 
doc_dir = "data/esmo"

#add nodes to pipeline
indexing_pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
indexing_pipeline.add_node(component=preprocessor, name="PreProcessor", inputs=["TextConverter"])
indexing_pipeline.add_node(component=document_store, name="DocumentStore", inputs=["PreProcessor"])


####BUILD DOCUMENT STORE ? DO I NEED THIS
#document_store = InMemoryDocumentStore(use_bm25=True)
#doc_dir = "data/esmo"
#output_dir = doc_dir
#files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
#indexing_pipeline = TextIndexingPipeline(document_store)
#indexing_pipeline.run_batch(file_paths=files_to_index)
####

##INDEX
files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
indexing_pipeline.run_batch(file_paths=files_to_index)

##INITIALIZE RETRIEVER

from haystack.nodes import BM25Retriever
retriever = BM25Retriever(document_store=document_store)

from haystack.nodes import EmbeddingRetriever
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.pipelines import ExtractiveQAPipeline

document_store = ElasticsearchDocumentStore(
    similarity="dot_product",
    embedding_dim=768
)
#EMBEDDING RETRIEVER WITH OPEN AI KEY
retriever = EmbeddingRetriever(
   document_store=document_store,
   batch_size=8,
   embedding_model="ada",
   api_key="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",
   max_seq_len=1024
)
document_store.update_embeddings(retriever)

##INITIALIZE READER
from haystack.nodes import FARMReader
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

##GET PIPELINE UP (RETRIEVER / READER)
from haystack import Pipeline

querying_pipeline = Pipeline()
querying_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
querying_pipeline.add_node(component=reader, name="Reader", inputs=["Retriever"])


prediction=""

def predictionModel(question):
    if not question:
        return "You forgot to ask a question..."
    
    prediction = querying_pipeline.run(
            query=question, 
            params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}
            }
    )
    pprint(prediction)
    return prediction


