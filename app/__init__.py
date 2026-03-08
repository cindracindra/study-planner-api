from fastapi import FastAPI

from app.api.confidence_ratings import confidence_ratings_router
from app.api.tasks import tasks_router
from app.api.banner import banner_router
from app.settings import Settings

tags_metadata = [
    {
        "name": "personal tasks",
        "description": "Summary and update of personal tasks and to-dos for the academic year",
    },
    {
        "name": "personal confidence ratings",
        "description": "Summary and update of personal confidence ratings for modules",
    },
    {
        "name": "banner",
        "description": "Fetch and update of quotes, excuse and custom quotes for banner",
    }
]


def create_application() -> FastAPI:
    rest_api: FastAPI = FastAPI(
        title="Study Planner API",
        description=(
            "SSE Project: API for study planner @ Department of Computing, Imperial College London"
        ),
        version="1.0",
        contact={
            "name": "Cindra",
            "email": "cindra.cindra4625@imperial.ac.uk",
        },
        servers=[{"url": Settings().server_url, "description": Settings().environment}],
        openapi_tags=tags_metadata,
        docs_url="/",
    )
    
    routers = [tasks_router, confidence_ratings_router, banner_router]
    
    for router in routers:
        rest_api.include_router(router)
        
    return rest_api
