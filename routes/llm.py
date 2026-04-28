import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

router = APIRouter(prefix="/llm", tags=["llm"])

# Initialize OpenAI LLM with langchain
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")


class QueryRequest(BaseModel):
    query: str
    system_prompt: str = "You are a helpful assistant. Provide clear and concise responses."


class QueryResponse(BaseModel):
    query: str
    response: str
    model: str = MODEL_NAME


def get_llm(streaming: bool = False):
    """Initialize and return LLM instance"""
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Set OPENAI_API_KEY environment variable."
        )
    return ChatOpenAI(
        model=MODEL_NAME,
        api_key=OPENAI_API_KEY,
        temperature=0.7,
        streaming=streaming
    )


def validate_query(query: str):
    if not query or len(query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query cannot be empty")


def create_messages(request: QueryRequest):
    return [
        SystemMessage(content=request.system_prompt),
        HumanMessage(content=request.query)
    ]


def chunk_to_text(chunk):
    content = chunk.content if hasattr(chunk, "content") else chunk
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            item if isinstance(item, str) else str(item.get("text", ""))
            for item in content
            if isinstance(item, (str, dict))
        )
    return str(content) if content else ""


@router.post("/query", response_model=QueryResponse)
def query_llm(request: QueryRequest):
    """
    Send a query to the LLM and get a response.
    
    Args:
        request: QueryRequest containing:
            - query (str): The question or prompt for the LLM
            - system_prompt (str, optional): System instructions for the LLM
    
    Returns:
        QueryResponse containing:
            - query: The original query
            - response: The LLM's response
            - model: The model used (gpt-3.5-turbo)
    """
    try:
        # Validate query
        validate_query(request.query)

        # Initialize LLM
        llm = get_llm()

        # Create messages
        messages = create_messages(request)

        # Get response from LLM
        response = llm.invoke(messages)

        # Extract response text
        response_text = response.content if hasattr(response, 'content') else str(response)

        return QueryResponse(
            query=request.query,
            response=response_text,
            model=MODEL_NAME
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error querying LLM: {str(e)}"
        )


@router.post("/query/stream")
def stream_query_llm(request: QueryRequest):
    """
    Stream an LLM response token by token.
    """
    try:
        validate_query(request.query)
        llm = get_llm(streaming=True)
        messages = create_messages(request)

        def generate_response():
            try:
                for chunk in llm.stream(messages):
                    text = chunk_to_text(chunk)
                    if text:
                        yield text
            except Exception as e:
                yield f"\n[Error querying LLM: {str(e)}]"

        return StreamingResponse(
            generate_response(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
            }
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error querying LLM: {str(e)}"
        )


@router.get("/health")
def health_check():
    """
    Check the health and configuration status of the LLM service.
    """
    if not OPENAI_API_KEY:
        return {
            "status": "unhealthy",
            "reason": "OpenAI API key not configured"
        }

    if not MODEL_NAME:
        return {
            "status": "unhealthy",
            "reason": "OpenAI model name not configured"
        }

    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "provider": "OpenAI"
    }
