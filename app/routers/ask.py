import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import AskRequest, AskResponse
from app.services.retriever import retrieve_context
from app.services.llm_service import get_chain
from app.config import settings

router = APIRouter()

def _prepare_rag_inputs(request: AskRequest):
    context_chunks = retrieve_context(request.question)
    context = "\n\n".join(context_chunks)
    inputs = {
        "name": settings.portfolio_owner_name,
        "context": context,
        "question": request.question,
    }
    return inputs, context_chunks

@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    inputs, context_chunks = _prepare_rag_inputs(request)
    chain = get_chain(streaming=False)
    answer = await chain.ainvoke(inputs)
    return AskResponse(answer=answer, sources=context_chunks)

@router.post("/ask/stream")
async def ask_stream(request: AskRequest):
    inputs, _ = _prepare_rag_inputs(request)
    chain = get_chain(streaming=True)

    async def event_generator():
        async for token in chain.astream(inputs):
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
