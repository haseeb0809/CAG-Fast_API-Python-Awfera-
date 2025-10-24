
# CAG Project - Chat With Your PDF 📄🤖

# Awfera Final Project Python Programming Course 

An AI-powered REST API that enables intelligent question-answering over PDF documents using Google's Gemini AI model.

## 🌟 Features

- **PDF Upload & Processing**: Extract text from PDF documents automatically
- **AI-Powered Q&A**: Ask questions about your documents using Google Gemini
- **User Management**: Associate documents with usernames for multi-user support
- **UUID-Based Storage**: Manage multiple documents independently
- **RESTful API**: Clean, well-documented endpoints with automatic Swagger UI
- **Comprehensive Validation**: File type, size, and content validation
- **Error Handling**: Proper HTTP status codes and descriptive error messages
- **Logging System**: Track all operations for debugging and monitoring## 📂 Project Structure

```
cag-pdf-chat/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
│
├── logs/                        # Application logs (auto-generated)
│   └── app_YYYYMMDD.log
│
└── src/                         # Source code
    ├── __init__.py
    ├── data_store.py            # In-memory data storage
    │
    ├── routers/                 # API endpoints
    │   ├── __init__.py
    │   └── data_handler.py      # CRUD operations
    │
    └── utils/                   # Utility functions
        ├── __init__.py
        ├── pdf_processor.py     # PDF text extraction
        ├── llm_client.py        # Gemini AI integration
        └── logger.py            # Logging configuration
            
```
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP Requests
       ▼
┌─────────────────────┐
│   FastAPI Server    │
│  ┌───────────────┐  │
│  │ Data Handler  │  │
│  │  (Routers)    │  │
│  └───────┬───────┘  │
│          │          │
│  ┌───────▼───────┐  │
│  │  PDF Parser   │  │
│  │   (PyPDF)     │  │
│  └───────────────┘  │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │ Google Gemini│
    │      AI      │
    └──────────────┘
```         

## Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern, fast web framework for building APIs
- **[PyPDF](https://pypdf.readthedocs.io/)**: PDF text extraction library
- **[Google Gemini AI](https://ai.google.dev/)**: Large language model for question answering
- **[Uvicorn](https://www.uvicorn.org/)**: ASGI server for running the application
- **[Python 3.11](https://www.python.org/)**: Programming language with type hints




### Logging

Logs are automatically created in the `logs/` directory with daily rotation:
- Location: `logs/app_YYYYMMDD.log`
- Format: `timestamp - module - level - message`
- Outputs: File and console
## Installation

1. **Clone the repository**  

```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
```
2. **Clone the repository**  
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3. **Install the required libraries**
All dependencies are listed in requirements.txt. Install them with
```
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a .env file in the project root and add your Google Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```
5. **Run the application**
Start the FastAPI server:
```
uvicorn main:p --reload
```


    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file


## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome page with documentation links |
| `POST` | `/api/v1/upload/{uuid}` | Upload a new PDF document |
| `PUT` | `/api/v1/update/{uuid}` | Append content to existing document |
| `GET` | `/api/v1/query/{uuid}` | Ask questions about the document |
| `DELETE` | `/api/v1/data/{uuid}` | Delete document data |
| `GET` | `/api/v1/list_uuids` | List all stored documents |

## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

##  Security Considerations & Limitations
## API Key: 
Keep your GEMINI_API_KEY secure and never commit it to version control
## File Size Limit:
Maximum upload size is 10MB
## File Type Validation: 
Only PDF files are accepted

## 
 📊 API Response Codes


| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created (upload successful) |
| 400 | Bad Request (invalid file type, empty file) |
| 403 | Forbidden (access denied) |
| 404 | Not Found (UUID doesn't exist) |
| 413 | Payload Too Large (file exceeds 10MB) |
| 422 | Unprocessable Entity (PDF has no extractable text) |
| 500 | Internal Server Error 