from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.templating import Jinja2Templates

from hotels.exceptions import LocationNotFound
from hotels.router import get_hotels, get_hotels_by_location

page_router = APIRouter(prefix="/pages", tags=["Frontend"])
templates = Jinja2Templates(directory="src/")


@page_router.get("/hotels")
async def get_hotels_page(request: Request):
    try:
        hotels = await get_hotels()
        return templates.TemplateResponse(name="hotels/templates/get_hotels.html",
                                          context={"request": request,
                                                   "hotels": hotels})
    except HTTPException as exc:
        return templates.TemplateResponse(name="templates/404_exception.html",
                                          context={"request": request,
                                                   "detail": exc.detail})


@page_router.get("/hotels/city")
async def get_hotels_by_location_page(request: Request,
                                      location: str = "Russia"):
    try:
        hotels = await get_hotels_by_location(location=location)
        if hotels:
            return templates.TemplateResponse(name="hotels/templates/get_hotels_by_location.html",
                                              context={"request": request,
                                                       "hotels": hotels,
                                                       "location": location})
    except HTTPException:
        return templates.TemplateResponse(name="hotels/templates/get_hotels_by_location.html",
                                          context={"request": request,
                                                   "location": location,
                                                   "detail": LocationNotFound().detail},
                                          status_code=404)
