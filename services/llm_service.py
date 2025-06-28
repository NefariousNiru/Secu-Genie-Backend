# backend/services/llm_service.py

import asyncio
from typing import AsyncGenerator, List, Tuple
from config.settings import settings


async def stream_chat(
    prompt: str, history: List[str], model_name: str
) -> AsyncGenerator[Tuple[str, str], None]:
    """
    Async generator that yields chat output as (token, final_text) tuples.

    - Streams individual tokens first (with empty final_text).
    - At the end, emits a tuple with final_text set to the entire response.

    This stub simply echoes the prompt character-by-character, then returns
    the full echo. Replace the stub logic with a llama.cpp or cloud API call.

    Args:
        prompt (str): The user’s current question or instruction.
        history (List[str]): Prior conversation turns (unused in stub).
        model_name (str): Identifier of the model to invoke (unused in stub).

    Yields:
        AsyncGenerator[Tuple[str, str], None]:
            - (token, "") for each streamed token.
            - ("", final_text) once, when the full response is ready.
    """
    # Construct a dummy response
    dummy_response = f"Echo: {prompt}"

    # Stream out one character at a time
    for char in dummy_response:
        await asyncio.sleep(0.01)  # simulate async token generation delay
        yield (char, "")  # streaming token

    # Finally, send the complete response
    yield ("", dummy_response)
