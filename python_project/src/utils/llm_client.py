import os
from google import genai
from google.genai import types
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())


def get_llm_response(context: str, query: str) -> str:
    """
    Send a user query and context to Google Gemini and return the assistant's nse.

    Args:
        context (str): Background information delimited by triple backticks.
        query (str): The user's question to be answered based on the context.

    returns:
        str: The assistant's generate text response.

    Raises:
        ValueError: if thr GEMINI_API_KEY env variable is not set.   
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set."
            "Please set it to your Google Gemini API key (get key from https://aistudio.google.com)"
        )

    # Initialize the GenAI client
    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=query)],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
    response_mime_type="text/plain",
    system_instruction=[
        types.Part.from_text(
            text=(
                "You are a helpful assistant that can answer questions based on the provided context, which is delimited "
                "with triple backticks.\n\n"
                "You will be given a context and a user query. Your task is to generate a response that is "
                "relevant to the query based on the context provided. If the context does not contain enough "
                "information to answer the query, you should indicate that you do not have enough information "
                "to provide a complete answer.\n\n"
                "If the context is empty, you should respond with a message indicating that there is not "
                "enough information to answer the query.\n\n"
                "You should always respond in a friendly and helpful manner and you should not include "
                "personal opinions or information in your responses.\n\n"
                f"Context:\n```{context}```"
            )
        )
    ]
)

    # Stream and accumulate the response
    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text

    return response_text