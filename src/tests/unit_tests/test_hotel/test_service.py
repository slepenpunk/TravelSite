import pytest

from hotels.service import HotelService


@pytest.mark.asyncio
async def test_get_hotels():
    get_hotels = await HotelService.find_all()
    assert get_hotels


@pytest.mark.asyncio
@pytest.mark.parametrize("city", [
    ("Сочи"),
    ("Несуществующий город"),
])
async def test_get_hotels_by_city(city: str):
    get_hotels = await HotelService.find_all(city=city)
    if get_hotels:
        assert get_hotels
        hotel_cities = [i.city for i in get_hotels]
        print(hotel_cities)
        assert city in hotel_cities
    else:
        assert not get_hotels



