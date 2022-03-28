from fastapi import FastAPI
from routes.annotate import router
from config.db import Settings

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Settings()
app.include_router(router)

if __name__ == "__main__":
    """
    Entrypoint for development and debugging purpose.
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
