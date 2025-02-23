# Medical Chatbot

A locally-hosted medical chatbot powered by Llama3 through Ollama, featuring context-aware responses and medical information retrieval.

## Architecture Flow

The chatbot follows a structured flow to process and respond to user queries:

```mermaid
flowchart TB
    Start([User Query]) --> Flask[Flask Web App]
    Flask --> LLM[Local Llama3 Model]
    
    LLM --> ContextCheck{Check Context\nHistory}
    
    ContextCheck -->|Has Context| GenerateAnswer[Generate Answer\nfrom Context]
    
    ContextCheck -->|No Context| MedCheck{Is Query\nMedical?}
    
    MedCheck -->|No| Reject[Return Non-Medical\nQuery Message]
    
    MedCheck -->|Yes| Search[DuckDuckGo Search]
    
    Search --> ProcessSearch[Process Search Results]
    
    ProcessSearch --> StructuredAnswer[Generate Structured\nAnswer]
    
    GenerateAnswer --> Response([Return Response to User])
    StructuredAnswer --> Response
    Reject --> Response
    
    style Start fill:#a8d5ff,color:#333333
    style Response fill:#a8d5ff,color:#333333
    style LLM fill:#ffe6cc,color:#333333
    style Flask fill:#d9ead3,color:#333333
    style Search fill:#fff2cc,color:#333333
    style ContextCheck fill:#f8cecc
    style MedCheck fill:#f8cecc
```

## How It Works

1. **User Interface**: Users interact with the chatbot through a Flask-based web interface.

2. **Query Processing**:
   - The query is processed by a locally running Llama3 model via Ollama
   - The system first checks the conversation history for relevant context

3. **Response Generation**:
   - If sufficient context exists, the bot generates an answer directly
   - If context is missing, the system verifies if the query is medical-related
   - Non-medical queries are rejected with an appropriate message
   - For valid medical queries without context, the system performs a DuckDuckGo search
   - Search results are processed and structured into a comprehensive response

## Features

- Local LLM hosting using Ollama
- Context-aware conversations
- Medical query validation
- Integration with DuckDuckGo for up-to-date medical information
- Web-based user interface

## Prerequisites

- Python 3.x
- Flask
- Ollama with Llama3 model
- Internet connection for DuckDuckGo searches

## Installation

[Add your installation instructions here]

## Usage

[Add your usage instructions here]

## Contributing

[Add your contribution guidelines here]

## License

[Add your license information here]
