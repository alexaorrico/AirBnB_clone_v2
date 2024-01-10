# Number of places to generate
num_places = 20

# Generate SQL statements for inserting data into the places table
insert_statements = []

for _ in range(num_places):
    place_id = str(uuid.uuid4())
    city_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    name = fake.bs()
    description = fake.paragraph()
    number_rooms = random.randint(1, 10)
    number_bathrooms = random.randint(1, 5)
    max_guest = random.randint(1, 10)
    price_by_night = random.randint(50, 500)
    latitude = round(random.uniform(30, 40), 6)
    longitude = round(random.uniform(-120, -70), 6)

    insert_sql = f"INSERT INTO `places` (id, created_at, updated_at, city_id, user_id, name, description, number_rooms, number_bathrooms, max_guest, price_by_night, latitude, longitude) VALUES ('{place_id}', NOW(), NOW(), '{city_id}', '{user_id}', '{name}', '{description}', {number_rooms}, {number_bathrooms}, {max_guest}, {price_by_night}, {latitude}, {longitude});"
    insert_statements.append(insert_sql)

# Print the SQL statements
for statement in insert_statements:
    print(statement)
