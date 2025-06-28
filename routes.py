from fastapi import FastAPI
from controllers.file_controller import file_controller


def register(app: FastAPI):
    app.include_router(file_controller)
