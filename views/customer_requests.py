import sqlite3
import json
from models import Customer

def get_all_customers():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT
                c.id,
                c.name,
                c.address,
                c.email,
                c.password
            FROM customer c
            """)

        # Initialize an empty list to hold all customer representations
        customers = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an customer instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # customer class above.
            customer = Customer(row['id'], row['name'], row['address'], row['email'], row['password'])

            customers.append(customer.__dict__) # see the notes below for an explanation on this line of code.

    return customers

def get_single_customer(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
            SELECT
                c.id,
                c.name,
                c.address,
                c.email,
                c.password
            FROM customer c
            WHERE c.id = ?
            """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an customer instance from the current row
        customer = Customer(data['id'], data['name'], data['address'], data['email'], data['password'])

        return customer.__dict__
        
def get_customer_by_email(email):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            select
                c.id,
                c.name,
                c.address,
                c.email,
                c.password
            from Customer c
            WHERE c.email = ?
            """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return customers

def create_customer(new_customer):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            INSERT INTO customer
                ( name, address, email, password )
            VALUES
                ( ?, ?, ?, ?);
            """, (new_customer['name'], new_customer['address'],
                new_customer['email'], new_customer['password'], ))

        id = db_cursor.lastrowid

        new_customer['id'] = id

    return new_customer

def delete_customer(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            DELETE FROM customer
            WHERE id = ?
            """, (id, ))

def update_customer(id, new_customer):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            UPDATE Customer
                SET
                    name = ?,
                    address = ?,
                    email = ?,
                    password = ?
            WHERE id = ?
            """, (new_customer['name'], new_customer['address'],
                new_customer['email'], new_customer['password'], id, ))

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