from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.exceptions import QuestionnaireNotFoundError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(QuestionnaireNotFoundError)
    async def survey_not_found_handler(request: Request, exc: QuestionnaireNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message, "error_code": "SURVEY_NOT_FOUND"},
        )
