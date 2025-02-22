from llm_interactions import is_medical_query_llm, has_context_to_answer
import ollama
from utils import web_search
import logging

def generate_response(query, conversation_history, context_message=None):
    logging.info("Generating response...")
    model_name = "llama3" 
    
    # Add the context message if provided
    if context_message:
        conversation_history = [{"role": "system", "content": context_message}] + conversation_history

    has_context = has_context_to_answer(query, conversation_history, model_name)

    if not has_context and not is_medical_query_llm(query, model_name):
        return "This chatbot only handles medical-related queries. Please ask a medical question."
    
    if not has_context:
        search_content = web_search(query)
        conversation_history.append({"role": "system", "content": search_content})

    # Generate the final response
    messages = conversation_history + [{"role": "user", "content": query}]
    response = ollama.chat(model=model_name, messages=messages)
    text_response = response.model_dump()["message"]["content"]
    logging.info("Response generated.")
    return text_response