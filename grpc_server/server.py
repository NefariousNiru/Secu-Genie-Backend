# backend/grpc_server/server.py

"""
GRPCServer sets up and manages the lifecycle of our gRPC aio server.

It:
  1. Registers the ChatServiceServicer implementation.
  2. Binds to settings.grpc_host:settings.grpc_port.
  3. Exposes start() and stop() methods for integration into FastAPI's lifespan.
"""

from grpc import aio
from config.settings import settings
from proto.chat_pb2_grpc import add_ChatServiceServicer_to_server
from grpc_server.servicer import ChatServiceServicerImpl

class GRPCServer:
    """
    Wrapper around grpc.aio.server for SecuGenie.

    Attributes:
        server (aio.Server): The underlying gRPC asynchronous server.
    """

    def __init__(self):
        # Create an aio server instance
        self.server = aio.server()
        # Register our ChatService implementation on this server
        add_ChatServiceServicer_to_server(
            ChatServiceServicerImpl(),
            self.server
        )

    async def start(self) -> None:
        """
        Start the gRPC server on the configured host and port.

        Uses:
            settings.grpc_host (str): Host address, e.g. "127.0.0.1"
            settings.grpc_port (int): Port number, e.g. 50051

        Raises:
            RuntimeError: If the server fails to bind or start.
        """
        listen_addr = f"{settings.grpc_host}:{settings.grpc_port}"
        # Bind insecure (no TLS) for local-only communication
        self.server.add_insecure_port(listen_addr)
        # Start serving RPCs
        await self.server.start()
        print(f"✅ gRPC server listening on {listen_addr}")

    async def stop(self, grace: int = 5) -> None:
        """
        Shutdown the gRPC server, waiting up to `grace` seconds for inflight RPCs.

        Args:
            grace (int): Maximum seconds to wait for ongoing RPCs to finish.
        """
        await self.server.stop(grace)
        print("🛑 gRPC server shut down")
