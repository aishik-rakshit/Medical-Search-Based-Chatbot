
# runner.py

from chatbot import generate_response
import logging

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
