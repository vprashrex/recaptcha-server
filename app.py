from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import requests
import json

server = FastAPI()

origins = [
    'http://localhost:3000'
]

server.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers = ["*"]
)


@server.post("/api/recaptcha")
async def resend_email(file:dict):
    try:
        URL = "https://www.google.com/recaptcha/api/siteverify"
        SECRET = "6Ld24oAmAAAAAAKDcqcL7B6OPEx5VKWyquJU6urG"
        TOKEN = file["token"]

        params = {
            "secret":SECRET,
            "response":TOKEN
        }
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"  # Set the CORS origin header
        }
        response = requests.post(URL,params=params,headers=headers)
        data = response.json()
        success = data["success"]
        score = data["score"]
        
        return JSONResponse(
            status_code=200,
            content={
                "success":success,
                "score":score
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "error":e
            }
        )