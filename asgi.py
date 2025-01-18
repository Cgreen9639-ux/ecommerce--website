from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from starlette.staticfiles import StaticFiles # type: ignore
from starlette.responses import FileResponse # type: ignore
import uvicorn # type: ignore

app = FastAPI()

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (e.g., frontend build)
import os

static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
index_file = os.path.join(static_dir, "index.html")
if not os.path.exists(index_file):
    with open(index_file, "w") as f:
        f.write("<html><body><h1>Hello, World!</h1></body></html>")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.get("/api/data")
async def get_data():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)

    