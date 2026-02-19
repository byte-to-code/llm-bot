from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

ROUTER = APIRouter(route_class=DishkaRoute)


@ROUTER.get("/health")
async def health():
    return {"status": "ok"}
