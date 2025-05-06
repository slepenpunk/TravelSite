from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates

from hotels.exceptions import CityNotFound
from hotels.router import get_hotels, get_hotels_by_city

page_router = APIRouter(prefix="/pages", tags=["Frontend"])
templates = Jinja2Templates(directory="src/")


@page_router.get("/hotels")
async def get_hotels_page(request: Request):
    try:
        hotels = await get_hotels()
        return templates.TemplateResponse(
            name="hotels/templates/get_hotels.html",
            context={"request": request, "hotels": hotels},
        )
    except HTTPException as exc:
        return templates.TemplateResponse(
            name="templates/404_exception.html",
            context={"request": request, "detail": exc.detail},
        )


@page_router.get("/hotels/city")
async def get_hotels_by_location_page(request: Request, city: str = "Москва"):
    try:
        hotels = await get_hotels_by_city(city=city)
        if hotels:
            return templates.TemplateResponse(
                name="hotels/templates/get_hotels_by_location.html",
                context={"request": request, "hotels": hotels, "city": city},
            )
    except HTTPException:
        return templates.TemplateResponse(
            name="hotels/templates/get_hotels_by_location.html",
            context={"request": request, "city": city, "detail": CityNotFound().detail},
            status_code=404,
        )
