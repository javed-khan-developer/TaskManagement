from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException

from utils.logger import logger


async def http_exception_handler(
    request: Request,
    exc: HTTPException
):

    logger.warning(exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail
        }
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )