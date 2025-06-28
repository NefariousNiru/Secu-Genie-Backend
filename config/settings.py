from pydantic.v1 import BaseSettings, Field
from pathlib import Path


class Settings(BaseSettings):
    # === gRPC Settings ===
    grpc_host: str = Field(
        default="127.0.0.1",
        description="Address where the gRPC server will listen",
        env="GRPC_HOST",
    )
    grpc_port: int = Field(
        default=50051,
        description="Port on which the gRPC service is exposed",
        env="GRPC_PORT",
    )

    # === Local model settings ===
    model_dir: Path = Field(
        default=Path.home() / ".secu-genie" / "models",
        description="Directory where user-downloaded GGUF models are stored",
    )

    # === FAISS index settings ===
    faiss_index_dir: Path = Field(
        default=Path.home() / ".secu-genie" / "faiss",
        description="Directory where FAISS index files are persisted",
    )
    faiss_index_file: str = Field(
        default="index.faiss", description="Filename for the FAISS index"
    )

    # === Chunking parameters ===
    chunk_size: int = Field(
        default=1000, description="Maximum characters per document chunk"
    )
    chunk_overlap: int = Field(
        default=200, description="Overlap characters between chunks"
    )

    # === Cloud Keys ===
    openai_api_key: str | None = Field(
        default=None,
        env="OPENAI_API_KEY",
        description="OpenAI API Key (optional for cloud mode)",
    )
    gemini_api_key: str | None = Field(
        default=None,
        env="Gemini_API_KEY",
        description="Gemini API Key (optional for cloud mode)",
    )
    pinecone_api_key: str | None = Field(
        default=None,
        env="PINECONE_API_KEY",
        description="Pinecone API Key (optional for cloud mode)",
    )
    pinecone_env: str | None = Field(
        default=None,
        env="PINECONE_ENV",
        description="Pinecone Environment name (optional for cloud mode)",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
