from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.user_router import router as user_router
from routers.auth_router import router as auth_router
from routers.task_router import router as task_router
from routers.file_router import router as file_router
from fastapi import Request
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(
    request: Request,
    call_next
):

    start = time.time()

    response = await call_next(request)

    end = time.time()

    print(
        f"{request.method} {request.url.path} took {end-start:.4f}s"
    )

    return response

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(file_router)