from contextlib import asynccontextmanager
from fastapi import FastAPI
import routes
from config.settings import settings
from grpc_server.server import GRPCServer

@asynccontextmanager
async def lifespan(fastApi: FastAPI):
    """
    FastAPI lifespan context that:
      1. Ensures model & FAISS directories exist.
      2. Starts the gRPC server.
      3. Yields control to run FastAPI.
      4. On shutdown, gracefully stops gRPC.
    """
    settings.model_dir.mkdir(parents=True, exist_ok=True)               # Check for local models
    settings.faiss_index_dir.mkdir(parents=True, exist_ok=True)         # Check for local faiss pickle
    grpc_server = GRPCServer()                                          # Instantiate gRPC
    await grpc_server.start()                                           # Start gRPC server

    yield

    await grpc_server.stop()                                            # Stop gRPC server on shutdown

app = FastAPI(title="SecuGenie Backend", lifespan=lifespan)
routes.register(app)