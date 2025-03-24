from fastapi import FastAPI
from src.equipments.router import equipments_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(equipments_router)
origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
