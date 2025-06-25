import grpc
from proto.chat_pb2 import ChatResponse
from proto.chat_pb2_grpc import ChatServiceServicer
from services.llm_service import stream_chat


class ChatServiceServicerImpl(ChatServiceServicer):
    """
    gRPC servicer that implements the ChatService defined in chat.proto.

    The StreamChat method receives a ChatRequest and yields ChatResponse
    messages, streaming tokens as they become available or the final text.
    """

    async def StreamChat(self, request, context):
        """
        Server‐side streaming handler for chat.

        Args:
            request (ChatRequest): Contains `prompt`, `history`, and `model`.
            context (grpc.aio.ServicerContext): RPC context (for metadata, cancellation).

        Yields:
            ChatResponse: One or more messages containing:
              - token: incremental token(s) if streaming
              - final_text: complete answer on the last message
        """
        # Extract fields from the request
        prompt = request.prompt
        history = list(request.history)
        model_name = request.model

        # Delegate to llm_service.stream_chat, which is an async generator
        async for token, final_text in stream_chat(prompt, history, model_name):
            # If we have a final_text, send it in the final response
            if final_text:
                yield ChatResponse(token="", final_text=final_text)
            else:
                yield ChatResponse(token=token, final_text="")

