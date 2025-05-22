import uvicorn

from fastapi import FastAPI
from src.equipments.router import equipments_router
from src.auth.router import auth_router
from src.events.router import events_router
from fastapi.middleware.cors import CORSMiddleware
from src.events.web_socket import web_socket_router
app = FastAPI()
app.include_router(equipments_router)
app.include_router(events_router)
app.include_router(auth_router)
app.include_router(web_socket_router)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5500",

]

app.add_middleware(

    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS", "DELETE", "PUT"],
    allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=False
    )
