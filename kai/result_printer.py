from typing import Dict, Any, List, Optional

import json
import pprint
import logging
from collections import defaultdict

import pandas as pd

from haystack.schema import Document, Answer, SpeechAnswer
from haystack.document_stores.sql import DocumentORM  #  type: ignore[attr-defined]

testCode = " { 'answer': 'The risk of fragility fracture in men on long-term ADT ' 'exceeds accepted intervention thresholds', 'context': 'The risk of fragility fracture in men on long-term ADT ' 'exceeds accepted intervention thresholds. Even before ' 'starting ADT, a large proportion of men d'}, { 'answer': 'Local salvage therapy', 'context': 'eir diagnostic performance, not their effect on care ' 'pathways.42\n' 'Local salvage therapy. The natural history of PSA ' 'recurrence following primary treatm'}, { 'answer': 'GETUG-12', 'context': 'rly docetaxel-based chemotherapy (ChT) in high-risk ' 'localised disease. GETUG-12 compared standard of care (ADT ' 'for 3 years plus RT) with or without 4 '}, { 'answer': 'STOMP trial', 'context': 'ecently, two randomised phase II trials have been ' 'published.47,48 The STOMP trial showed an improved ' 'biochemical progression and time to palliative AD'}, { 'answer': 'randomised 970 men with locally advanced disease to receive ' 'either 6 months or 36 months of ADT in addition to radical ' 'RT.26 The 5-year overall mortality for short-term and ' 'long-term sup- pression was 19.0% and 15.2%, respectively ' '(HR 1.42; CI 1.09e1.85).\n' 'A recent RCT evaluated 18 versus 36 months’ adjuvant ADT in ' '630 men with high-risk prostate cancer.27', 'context': ' randomised 970 men with locally advanced disease to ' 'receive either 6 months or 36 months of ADT in addition to ' 'radical RT.26 The 5-year overall mortality for short-term ' 'and long-term sup- pression was 19.0% and 15.2%, ' 'respectively (HR 1.42; CI 1.09e1.85).\n' 'A recent RCT evaluated 18 versus 36 months’ adjuvant ADT ' 'in 630 men with high-risk prostate cancer.27'}]"



def print_answers2(results: dict, details: str = "all", max_text_len: Optional[int] = None):
    """
    Utility function to print results of Haystack pipelines
    :param results: Results that the pipeline returned.
    :param details: Defines the level of details to print. Possible values: minimum, medium, all.
    :param max_text_len: Specifies the maximum allowed length for a text field. If you don't want to shorten the text, set this value to None.
    :return: None
    """
    #print("Sam WOrkings : See results")
    #print(results)
    
    # Defines the fields to keep in the Answer for each detail level
    fields_to_keep_by_level = {
        "minimum": {
            Answer: ["answer", "context"],
            SpeechAnswer: ["answer", "answer_audio", "context", "context_audio"],
        },
        "medium": {
            Answer: ["answer", "context", "score"],
            SpeechAnswer: ["answer", "answer_audio", "context", "context_audio", "score"],
        },
    }

    if not "answers" in results.keys():
        raise ValueError(
            "The results object does not seem to come from a Reader: "
            f"it does not contain the 'answers' key, but only: {results.keys()}.  "
            "Try print_documents or print_questions."
        )

    pp = pprint.PrettyPrinter(indent=4)

    queries = []
    if "query" in results.keys():  # results came from a `run` call
        #print("in query : run call : \n ")
        queries = [results["query"]]
        #print(queries)
        answers_lists = [results["answers"]]
        #print(answers_lists)

    elif "queries" in results.keys():  # results came from a `run_batch` call
        queries = results["queries"]
        answers_lists = results["answers"]

    for query_idx, answers in enumerate(answers_lists):
        # Filter the results by detail level
        filtered_answers = []
        if details in fields_to_keep_by_level.keys():
            for ans in answers:
                filtered_ans = {
                    field: getattr(ans, field)
                    for field in fields_to_keep_by_level[details][type(ans)]
                    if getattr(ans, field) is not None
                }
                filtered_answers.append(filtered_ans)
        elif details == "all":
            filtered_answers = answers
        else:
            valid_values = ", ".join(fields_to_keep_by_level.keys()) + " and 'all'"
            logging.warn("print_answers received details='%s', which was not understood. ", details)
            logging.warn("Valid values are %s. Using 'all'.", valid_values)
            filtered_answers = answers

        # Shorten long text fields
        if max_text_len is not None:
            for ans in answers:
                if getattr(ans, "context") and len(ans.context) > max_text_len:
                    ans.context = ans.context[:max_text_len] + "..."

        if len(queries) > 0:
            pp.pprint(f"Query: {queries[query_idx]}")
        pp.pprint("Answers:")
        
        print("END OUTPUT :")
        trythis = pp.pprint(filtered_answers)
        
        
        return(pp.pformat(filtered_answers))
    
