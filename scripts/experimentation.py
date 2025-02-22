import duckduckgo_search
import ollama
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def web_search(query):
    logging.info("Performing web search...")
    ddg = duckduckgo_search.DDGS()
    results = ddg.text(query)
    search_content = " ".join([result['body'] for result in results if 'body' in result])
    logging.info("Web search completed.")
    return search_content

def is_medical_query_llm(query, model_name):
    logging.info("Determining if the query is medical...")
    messages = [{"role": "system", "content": "Determine if the following query is medical: {query}. Respond with 'Yes' or 'No'."},
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

def generate_response(query, conversation_history, context_message=None):
    logging.info("Generating response...")
    model_name = "llama3"  # Replace with the actual model name

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

def main():
    conversation_history = []
    context_message = ("As a medical chatbot, I am here to provide accurate and reliable information "
                       "exclusively about medical needs. It is very important to check the previous search context "
                       "to determine if new information is required. If more information is needed, the chatbot should "
                       "respond with: 'I need more information.'")

    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit"]:
            logging.info("Exiting...")
            break
        response = generate_response(user_query, conversation_history, context_message)
        print(f"Chatbot: {response}")
        conversation_history.append({"role": "user", "content": user_query})
        conversation_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    logging.info("Starting chatbot...")
    main()