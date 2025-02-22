# utils.py

import logging
import duckduckgo_search

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def web_search(query):
    logging.info("Performing web search...")
    ddg = duckduckgo_search.DDGS()
    results = ddg.text(query)
    search_content = " ".join([result['body'] for result in results if 'body' in result])
    logging.info("Web search completed.")
    return search_content
