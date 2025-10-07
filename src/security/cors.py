from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



def configure_middleware(app : FastAPI):
    """
    CORSMiddleware : configure the allowance requests to get info from application
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # or specific IPs
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],  # <== THIS MUST INCLUDE 'authorization'
    )