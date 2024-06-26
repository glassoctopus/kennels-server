import sqlite3
import json
from models import Animal, Location, Customer

def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.location_id,
                a.customer_id,
                l.name location_name,
                l.address location_address,
                c.name customer_name,
                c.address customer_address,
                c.email customer_email      
            FROM Animal a
            JOIN Location l
                ON l.id = a.location_id
            JOIN Customer c 
                ON a.customer_id = c.id
            """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                            row['location_id'], row['customer_id'])
            
            # Create a Location instance from the current row
            location = Location(row['location_id'], row['location_name'], row['location_address'])
            
            # Customer instance ;^)
            customer = Customer(row['customer_id'], row['customer_name'], row['customer_address'], row['customer_email'])
            # remove the password property for output, write a discussion ticket to have teachers elaborate. 
            del customer.password

            # Add the dictionary representation of the location & customer to the animal
            animal.location = location.__dict__
            animal.customer = customer.__dict__

            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)
        
        return animals

def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.customer_id,
                a.location_id
            FROM animal a
            WHERE a.id = ?
            """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['customer_id'],
                            data['location_id'])

        return animal.__dict__

def get_animals_by_location(location):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.customer_id,
                a.location_id
            FROM animal a
            WHERE a.location_id = ?
            """, ( location, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['customer_id'], row['location_id'])
            animals.append(animal.__dict__)

    return animals

def get_animals_by_treatment(treatment):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.customer_id,
                a.location_id
            FROM animal a
            WHERE a.status = ?
            """, ( treatment, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['customer_id'], row['location_id'])
            animals.append(animal.__dict__)

    return animals    

def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            INSERT INTO Animal
                ( name, breed, status, location_id, customer_id )
            VALUES
                ( ?, ?, ?, ?, ?);
            """, (new_animal['name'], new_animal['breed'],
                new_animal['status'], new_animal['locationId'],
                new_animal['customerId'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id


    return new_animal

def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))
        
def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            UPDATE Animal
                SET
                    name = ?,
                    breed = ?,
                    status = ?,
                    location_id = ?,
                    customer_id = ?
            WHERE id = ?
            """, (new_animal['name'], new_animal['breed'],
                new_animal['status'], new_animal['location_id'],
                new_animal['customer_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    # return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def search_animal(search_string):
    searching_for = search_string
    print(searching_for, " is what we are searching for")
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
            SELECT
            *
            FROM animal a
            WHERE a.name LIKE ?
            """, ( '%' + search_string + '%', ))
        
        animals = []

        # Load the single result into memory
        search_data = db_cursor.fetchone()

        # Create an animal instance from the current row
        if search_data is not None:
            for row in search_data:
                animal = Animal(search_data['id'], search_data['name'], search_data['breed'],
                                search_data['status'], search_data['customer_id'],
                                search_data['location_id'])
                animals.append(animal.__dict__)
        
        
        db_cursor.execute("""
            SELECT
            *
            FROM animal a
            WHERE a.breed LIKE ?
            """, ( '%' + search_string + '%', ))
        
        breed_data = db_cursor.fetchone()

        if breed_data is not None:
            for row in breed_data:
                animal = Animal(breed_data['id'], breed_data['name'], breed_data['breed'],
                                breed_data['status'], breed_data['customer_id'],
                                breed_data['location_id'])
                animals.append(animal.__dict__)
        
        return animal.__dict__
    