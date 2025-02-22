# llm_interactions.py

import ollama
import logging

def is_medical_query_llm(query, model_name):
    logging.info("Determining if the query is medical...")
    messages = [{"role": "system", "content": f"Determine if the following query is medical: {query}. Respond with 'Yes' or 'No'."},
                {"role": "user", "content": query}]
    response = ollama.chat(model=model_name, messages=messages)
    is_medical = response.model_dump()["message"]["content"].strip().lower() == "yes"
    logging.info(f"Query is medical: {is_medical}")
    return is_medical

def has_context_to_answer(query, conversation_history, model_name):
    logging.info("Checking if the chat history has context to answer the question...")
    messages = conversation_history + [{"role": "user", "content": f"Based on the previous conversation, can you answer: {query}? Respond with 'Yes' or 'No'."}]
    response = ollama.chat(model=model_name, messages=messages)
    can_answer = response.model_dump()["message"]["content"].strip().lower() == "yes"
    logging.info(f"Chat history has context to answer the question: {can_answer}")
    return can_answer
