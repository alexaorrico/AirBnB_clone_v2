#!/usr/bin/python3
"""create some dummy data for file storage"""

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.review import Review
from os import remove


# clear storage
try:
    remove('file.json')
except FileNotFoundError:
    pass


# create users
DustinHoffman = User(
    id='DustinHoffman',
    first='Dustin',
    last='Hoffman',
    email='oj@ifki.sx',
    password='1Oe9QL0S'
)
DustinHoffman.save()
JoseDiaz = User(
    id='JoseDiaz',
    first='Jose',
    last='Diaz',
    email='bavim@poki.hk',
    password='JruQacG3'
)
JoseDiaz.save()
GeorgeStewart = User(
    id='GeorgeStewart',
    first='George',
    last='Stewart',
    email='suhehedet@nec.tg',
    password='WSzWNUE5'
)

# create states
NewYork = State(id='NY', name='New York')
NewYork.save()
Florida = State(id='Florida', name='Florida')
Florida.save()
California = State(id='California', name='California')
California.save()

# create cities
Miami = City(id='Miami', name='Miami', state_id='Florida')
Miami.save()
NewYorkCity = City(id='NewYorkCity', name='New York City', state_id='NY')
NewYorkCity.save()
Albany = City(id='Albany', name='Albany', state_id='NY')
Albany.save()
FortMyers = City(id='FortMyers', name='Fort Myers', state_id='Florida')
FortMyers.save()
Tampa = City(id='Tampa', name='Tampa', state_id='Florida')
Tampa.save()
SanDiego = City(id='SanDiego', name='San Diego', state_id='California')
SanDiego.save()
CaliforniaCity = City(id='CaliforniaCity',
                      name='California City', state_id='California')
CaliforniaCity.save()

# create amenities
Wifi = Amenity(name='WiFi', id='WiFi')
Wifi.save()
Pool = Amenity(name='Pool', id='Pool')
Pool.save()
InRoomCocktailStation = Amenity(
    name='In-Room Cocktail Station', id='CocktailStation')
InRoomCocktailStation.save()
MobileCheckIn = Amenity(name='Mobile Check-In', id='MobileCheck-In')
MobileCheckIn.save()
Bar = Amenity(name='Bar', id='Bar')
Bar.save()


# create place
Yotel = Place(
    id='Yotel',
    city_id='NewYorkCity',
    user_id='DustinHoffman',
    name='Yotel',
    description='Temporibus libero voluptatem cumque.',
    number_rooms=1,
    number_bathrooms=1,
    max_guest=2,
    price_by_night=104,
    longitude=58.6216,
    latitude=344.4797,
    amenity_ids=['WiFi', 'Pool']
)
Yotel.save()
Marriott = Place(
    id='Marriott',
    city_id='Orlando',
    user_id='GeorgeStewart',
    name='Marriott',
    description='Sapiente consequatur assumenda esse nulla necessitatibus.',
    number_rooms=2,
    number_bathrooms=2,
    max_guest=4,
    price_by_night=311,
    longitude=92.1057,
    latitude=259.9597,
    amenity_ids=['Bar', 'Pool', 'CocktailStation']
)
Marriott.save()
HolidayInn = Place(
    id='HolidayInn',
    city_id='FortMyers',
    user_id='JoseDiaz',
    name='HolidayInn',
    description='Voluptatem laboriosam mollitia veniam est.',
    number_rooms=3,
    number_bathrooms=2,
    max_guest=7,
    price_by_night=400,
    longitude=42.0188,
    latitude=38.183,
    amenity_ids=['WiFi', 'MobileCheck-In', 'Pool']
)
HolidayInn.save()

# create reviews
Review1 = Review(
    user_id='GeorgeStewart',
    place_id='Yotel',
    text='Eius occaecati exercitationem totam beatae aut in commodi.',
    id='Review1'
)
Review1.save()
Review2 = Review(user_id='GeorgeStewart',
    place_id='Marriott',
    text='Numquam adipisci est debitis.',
    id='Review2'
)
Review2.save()
Review3 = Review(user_id='JoseDiaz',
    place_id='HolidayInn',
    text='Et nisi sit inventore non.',
    id='Review3'
)
Review3.save()
