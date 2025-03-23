from fastapi import FastAPI
from src.equipments.router import equipments_router
app = FastAPI()
app.include_router(equipments_router)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
