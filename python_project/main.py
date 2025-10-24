from fastapi import FastAPI
from src.routers import data_handler
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="CAG Project API Chat With Your PDF",
    description="API for uploading PDFs, querying content via LLM, and managing data.",
    version="0.0.1",
)

app.include_router(
    data_handler.router,
    prefix="/api/v1",
    tags=["Data Handling And Chat with PDF"],
)

@app.get("/", response_class=HTMLResponse, tags=["Root"])
def read_root():
    """
    Provides a simple HTML welcome page with a link to swagger (OpenAPI) docs.
    """
    html_content = """
<!DOCTYPE html>
<html>
  <head>
    <title>CAG Project API</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        padding: 2rem;
        background: #f9f9f9;
        color: #222;
      }
      .container {
        max-width: 800px;
        margin: 0 auto;
        background: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
      }
      h1 {
        font-size: 2rem;
        margin-bottom: 1rem;
      }
      .emoji {
        margin-right: 0.5rem;
      }
      a {
        color: #007bff;
        text-decoration: none;
        font-weight: bold;
      }
      a:hover {
        text-decoration: underline;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Welcome to the CAG Project API</h1>
      <p>👉 View the automatically generated API documentation here:</p>
      <p><a href="/docs" target="_blank">Swagger UI (OpenAPI Docs)</a></p>
    </div>
  </body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host="127.0.0.1", port=8001
    )