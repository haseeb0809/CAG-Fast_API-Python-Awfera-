from fastapi import APIRouter, UploadFile, File, HTTPException, Query

from src.utils.logger import get_logger   # Import the custom logger function from the logger utility module

logger = get_logger(__name__)

import uuid as uuid_pkg 

from datetime import datetime
import os

# import the shared data stored 
from src.data_store import data_store

# pdf processing utility 
from src.utils.pdf_processor import extract_text_from_pdf

# LLM client utility
from src.utils.llm_client import get_llm_response 

router = APIRouter()

# define temp directory for uploads
UPLOAD_DIR = "/temp/cag_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
#File size limit 10MB
MAX_FILE_SIZE = 10*1024*1024
@router.post("/upload/{uuid}", status_code=201)
def upload_pdf(
    uuid: uuid_pkg.UUID, 
    username: str = Query(..., min_length=3, max_length=50),
    file: UploadFile = File(...)
):
    """
    Uploads a PDF file associated with a specific UUID.
    Extracts text from the PDF and stores it in the data store.
    If the UUID already exists, it raises an error (use PUT to update).
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDF files are accepted."
        )
    
    uuid_str = str(uuid) #convert uuid into str to store in system
    logger.info(f"Upload request received for UUID: {uuid_str}, file: {file.filename}")
    if uuid_str in data_store:
        raise HTTPException(
            status_code=400,
            detail=f"UUID {uuid_str} already exists. Use PUT /api/v1/update/{uuid_str} to append data.",
        )
    # Validate file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024):.0f}MB"
        )
    
    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )
    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str}_{file.filename}")
    try:
    # Save the uploaded file temporarily
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

    # Extract text using the utility function
        extracted_text = extract_text_from_pdf(file_path)

        if not extracted_text or extracted_text.strip() =="":
            raise HTTPException(
            status_code=422, detail="PDF Contain no extractable text."
        )

    # Store the extracted text with username
        data_store[uuid_str] = {
    "username": username,
    "content": extracted_text,
    "created_at": datetime.now().isoformat(),
    "file_count": 1
}
        logger.info(f"Successfully processed and stored PDF for UUID: {uuid_str}")
        return {
        "message": "File uploaded and text extracted successfully",
        "uuid": uuid_str,
    }

    except HTTPException:
        logger.error(f"Error processing PDF for UUID {uuid_str}: {str(e)}", exc_info=True)

        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during file processing: {str(e)}"
        )
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)


@router.put("/update/{uuid}")
def update_pdf_data(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):
    """
    Appends text extracted from a new PDF file to the existing data for a given UUID.
    If the UUID does not exist, it raises an error.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDF files are accepted"
        )

    uuid_str = str(uuid)
    logger.info(f"Update request received for UUID: {uuid_str}")
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404,
            detail=f"UUID {uuid_str} not found. Use POST /api/v1/upload/{uuid_str} to create it first.",
        )

    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str}_update_{file.filename}")
    try:
    # Save the uploaded file temporarily
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

    # Extract text from the new PDF
        new_text = extract_text_from_pdf(file_path)

        if new_text is None:
            raise HTTPException(
                status_code=500, detail="Failed to extract text from PDF."
            )
        
        # Append the new text (add a separator for clarity)
        data_store[uuid_str]["content"] += "\n\n" + new_text
        data_store[uuid_str]["file_count"] += 1
        logger.info(f"Successfully appended data to UUID: {uuid_str}")
        return {"message": "Data appended successfully", "uuid": uuid_str}

    except Exception as e:
        logger.error(f'Error updating PDF for UUID {uuid_str}: {str(e)}", exc_info=True')
        # Log the exception e
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during file processing: {str(e)}",
        )
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/query/{uuid}")
def query_data(
    uuid: uuid_pkg.UUID, 
    query: str = Query(..., min_length=1),
    username: str = Query(None)
):
    """
    Retrieves the stored text for a given UUID and sends it along with a query
    to the LLM service. Optionally verifies username for access control.
    """
    uuid_str = str(uuid)
    
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404, detail=f"UUID {uuid_str} not found."
        )
    
    # Get document data (now it's a dict)
    document = data_store[uuid_str]
    
    # Optional: Verify ownership
    if username:
        if document["username"] != username:
            raise HTTPException(
                status_code=403,
                detail="Access denied. This document belongs to another user."
            )
    
    # Extract content from document
    stored_text = document["content"]
    
    # Get LLM response
    llm_response = get_llm_response(context=stored_text, query=query)
    
    # Return comprehensive response
    return {
        "uuid": uuid_str,
        "username": document["username"],
        "query": query,
        "llm_response": llm_response
    }


@router.delete("/data/{uuid}", status_code=200)
def delete_data(uuid: uuid_pkg.UUID):
    """
    Deletes the data associated with a specific UUID from the data store.
    """
    uuid_str = str(uuid)
    logger.info(f"Deleting data for UUID: {uuid_str}")

    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404, detail=f"UUID {uuid_str}  not found."
        )

    del data_store[uuid_str]
    return {"message": f"Data for UUID {uuid_str}  deleted successfully."}


@router.get("/list_uuids")
def list_all_uuids():
    """
    Returns a list of all UUIDs with their usernames.
    """
    documents = [
        {
            "uuid": uuid,
            "username": data["username"],
            "created_at": data.get("created_at"),
            "file_count": data.get("file_count", 1)
        }
        for uuid, data in data_store.items()
    ]
    return {"documents": documents, "total": len(documents)}