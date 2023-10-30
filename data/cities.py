import random
import uuid
from faker import Faker

# Initialize Faker for generating random data
fake = Faker()

# Number of cities to generate
num_cities = 10

# Generate SQL statements for inserting data into the cities table
insert_statements = []

for _ in range(num_cities):
    city_id = str(uuid.uuid4())
    state_id = str(uuid.uuid4())
    city_name = fake.city()

    insert_sql = f"INSERT INTO `cities` (id, created_at, updated_at, name, state_id) VALUES ('{city_id}', NOW(), NOW(), '{city_name}', '{state_id}');"
    insert_statements.append(insert_sql)

# Print the SQL statements
for statement in insert_statements:
    print(statement)
