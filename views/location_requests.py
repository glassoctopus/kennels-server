import sqlite3
import json
from models import Location, Employee, Animal

def get_all_locations():
    """query to get all locations with their respective animals and employees"""
    # Initialize empty lists to hold all list representations for the complex request
    locations = []

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

def create_location(new_location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            INSERT INTO location
                ( name, address )
            VALUES
                ( ?, ? );
            """, (new_location['name'], new_location['address'], ))

        id = db_cursor.lastrowid

        new_location['id'] = id

    return new_location

def delete_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            DELETE FROM location
            WHERE id = ?
            """, (id, ))

def update_location(id, new_location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            UPDATE Location
                SET
                    name = ?,
                    address = ?
            WHERE id = ?
            """, (new_location['name'], new_location['address'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True