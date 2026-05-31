from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from routes.user import router

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", port=8000, host="0.0.0.0", reload=True, forwarded_allow_ips="*"
    )
