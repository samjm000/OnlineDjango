import logging
import os
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
import asyncio
import time
#from kai.pinecone_system import initiate_pinecone
from haystack import Pipeline

from haystack.document_stores import PineconeDocumentStore
####REMOVE
def initiate_pinecone():
    print("Testing PInecone")
    ENV="eu-west1-gcp"
    API="0c463aad-1d8d-498d-a28a-177dcfd12711"
    document_store = PineconeDocumentStore(
        api_key=API,
        index='esmo', 
        environment=ENV,
        
    )
    return document_store
####REMOVE

# LOGGING
logging.basicConfig(
    format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING
)
logging.getLogger("haystack").setLevel(logging.INFO)

# DOC STORE
document_store = initiate_pinecone()

from haystack.nodes import TextConverter, PDFToTextConverter, DocxToTextConverter, PreProcessor
from haystack.utils import convert_files_to_docs

# DATA to DOCS
# DATA to DOCS
doc_dir = "data/esmo"
#converter = TextConverter(remove_numeric_tables=True, valid_languages=["en"])
#doc_txt = converter.convert(file_path="data/esmo", meta=None)[0]
all_docs = convert_files_to_docs(dir_path=doc_dir)

## PRE-PROCESSOR
from haystack.nodes import PreProcessor
preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=False,
    split_by="word",
    split_length=150,
    split_respect_sentence_boundary=True,
    split_overlap=0
)
processed_esmo_docs = preprocessor.process(all_docs)
print(f"n_files_input: {len(all_docs)}\nn_docs_output: {len(processed_esmo_docs)}")
print(processed_esmo_docs[0])
# write document objects into document store
import os
from haystack.pipelines.standard_pipelines import TextIndexingPipeline

files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
indexing_pipeline = TextIndexingPipeline(document_store)
indexing_pipeline.run_batch(file_paths=files_to_index)

from haystack.nodes import DensePassageRetriever
retriever = DensePassageRetriever(
    document_store=document_store,
    #document_store=all_docs,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    max_seq_len_query=64,
    max_seq_len_passage=256,
    batch_size=2,
    use_gpu=True,
    embed_title=True,
    use_fast_tokenizers=True)

##INITIALIZE READER
from haystack.nodes import FARMReader
reader = FARMReader(model_name_or_path="dmis-lab/biobert-large-cased-v1.1-squad", use_gpu=True)

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
