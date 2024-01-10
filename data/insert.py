#!/usr/bin/python3

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

# Now you should be able to import your modules from the models package
import models
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Initialize Faker
fake = Faker()

# Create a database connection
engine = create_engine("mysql://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db")

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


# Generate random data and insert into tables
def create_fake_users(num_users):
    for _ in range(num_users):
        user = User(
            email=fake.email(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        session.add(user)


def create_fake_states(num_states):
    for _ in range(num_states):
        state = State(name=fake.state())
        session.add(state)


def create_fake_cities(num_cities, states):
    for _ in range(num_cities):
        city = City(name=fake.city(), state_id=random.choice(states).id)
        session.add(city)


def create_fake_amenities(num_amenities):
    for _ in range(num_amenities):
        amenity = Amenity(name=fake.word())
        session.add(amenity)


def create_fake_places(num_places, cities, users):
    for _ in range(num_places):
        place = Place(
            city_id=random.choice(cities).id,
            user_id=random.choice(users).id,
            name=fake.catch_phrase(),
            description=fake.text(),
            number_rooms=random.randint(1, 10),
            number_bathrooms=random.randint(1, 5),
            max_guest=random.randint(1, 10),
            price_by_night=random.randint(50, 300),
            latitude=random.uniform(10, 90),
            longitude=random.uniform(-180, 180),
        )
        session.add(place)


def create_fake_reviews(num_reviews, places, users):
    for _ in range(num_reviews):
        review = Review(
            place_id=random.choice(places).id,
            user_id=random.choice(users).id,
            text=fake.paragraph(),
        )
        session.add(review)


if __name__ == "__main__":
    # Define the number of fake records you want to generate
    num_fake_users = 10
    num_fake_states = 5
    num_fake_cities = 20
    num_fake_amenities = 30
    num_fake_places = 50
    num_fake_reviews = 100

    # Insert random data into all tables
    create_fake_users(num_fake_users)
    create_fake_states(num_fake_states)

    # Get the list of created users and states
    users = session.query(User).all()
    states = session.query(State).all()

    create_fake_cities(num_fake_cities, states)
    create_fake_amenities(num_fake_amenities)

    # Get the list of created cities
    cities = session.query(City).all()

    create_fake_places(num_fake_places, cities, users)
    create_fake_reviews(num_fake_reviews, session.query(Place).all(), users)

    # Commit and close the session
    session.commit()
    session.close()
