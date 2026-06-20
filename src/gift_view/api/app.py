from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from gift_view.api.routers import gifts


app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.include_router(gifts.router)
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

