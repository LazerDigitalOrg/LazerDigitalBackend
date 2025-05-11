from fastapi import FastAPI
from src.equipments.router import equipments_router
from src.auth.router import auth_router
from src.events.router import events_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(equipments_router)
app.include_router(events_router)
app.include_router(auth_router)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5500",
]

app.add_middleware(

    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS", "DELETE","PUT"],
    allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin',
                   'Access-Control-Allow-Credentials'],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
