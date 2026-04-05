from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

ROUTER = APIRouter(route_class=DishkaRoute)


@ROUTER.get("/get-all")
async def get_all_users():
    return {"status": "ok"}
