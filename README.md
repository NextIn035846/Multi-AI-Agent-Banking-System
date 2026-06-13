# Multi-AI Agent Banking System

An intelligent, conversational, and secure Multi-Agent AI System that automates retail banking queries using Streamlit, LangChain, and LangGraph.

## System Architecture

```
                      [ User Query ]
                             │
                             ▼
                 [ Secure Guardrail Layer ] (PII Masking)
                             │
                             ▼
                    [ Supervisor Agent ] (Intent & Entity Router)
            ┌────────────────┼────────────────┬────────────────┐
            │                │                │                │
            ▼                ▼                ▼                ▼
     [ Agent 1: RAG ] [ Agent 2: Core ] [ Agent 3: Lead ] [ Fallback Agent ]
     (FAQs & Policies) (Account Details) (Onboarding/DB)   (Human Handoff)
```

## Features

✅ **Supervisor-Worker Pattern**: Intelligent routing based on intent and entity recognition
✅ **RAG Specialist**: Retrieves banking policies and FAQs from vector database
✅ **Core Banking Agent**: Fetches real-time account details and transaction history
✅ **Onboarding Agent**: Manages new account creation with slot-filling
✅ **Fallback Agent**: Escalates to human agents when needed
✅ **PII Masking**: Automatic data protection for GDPR/PCI DSS compliance
✅ **Secure API Integration**: Decoupled authentication and database operations

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

## Configuration

Set environment variables in `.env`:

```
OPENAI_API_KEY=your_key_here
BANKING_API_URL=http://localhost:8000
VECTOR_DB_URL=localhost:6333
DATABASE_URL=postgresql://user:password@localhost/banking
```

## Project Structure

- `app.py` - Main Streamlit application
- `config.py` - Configuration settings
- `agents/` - Agent implementations
- `tools/` - Tool definitions for agents
- `security/` - PII masking and security utilities
- `api/` - Backend API client
- `data/` - Sample data and vector embeddings
