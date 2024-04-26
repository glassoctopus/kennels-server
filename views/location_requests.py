import sqlite3
import json
from models import Location, Employee, Animal

def get_all_locations():
    """query to get all locations with their respective animals and employees"""
    # Initialize empty lists to hold all list representations for the complex request
    locations = []
    employees = []
    animals = []

    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        """)
        
        dataset_locations = db_cursor.fetchall()     

        # Iterate list of data returned from database
        for row in dataset_locations:
            location = Location(row['id'], row['name'], row['address'])
            
            db_cursor.execute("""
            SELECT
                e.id,
                e.name,
                e.address,
                e.location_id
            FROM employee e
            WHERE e.location_id = ?
            """, ( location.id, ))
            
            dataset_employees = db_cursor.fetchall()
            
            for employee_row in dataset_employees:
                employee = Employee(employee_row['id'], employee_row['name'], employee_row['address'], employee_row['location_id'])
                location.employees.append(employee.__dict__)
                
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.location_id,
                a.customer_id
            FROM animal a
            WHERE a.location_id = ?
            """, ( location.id, ))
                
            dataset_animals = db_cursor.fetchall()
                
            for animal_row in dataset_animals:
                animal = Animal(animal_row['id'], animal_row['name'], animal_row['breed'], animal_row['status'], animal_row['location_id'], animal_row['customer_id'])
                location.animals.append(animal.__dict__)

            locations.append(location.__dict__) # see the notes below for an explanation on this line of code.

    return locations

def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        WHERE l.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an location instance from the current row
        location = Location(data['id'], data['name'], data['address'])

        return location.__dict__

def create_location(location):
    # Get the id value of the last location in the list
    max_id = LOCATIONS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the location dictionary
    location["id"] = new_id

    # Add the location dictionary to the list
    LOCATIONS.append(location)

    # Return the dictionary with `id` property added
    return location

def delete_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM location
        WHERE id = ?
        """, (id, ))

def update_location(id, new_location):
    # Iterate the locationS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the location. Update the value.
            new_location["id"] = id
            LOCATIONS[index] = new_location
            break    
    else:
        create_location(new_location) 