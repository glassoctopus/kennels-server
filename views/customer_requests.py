CUSTOMERS = [
    {
        "id": 1,
        "name": "Solie Juniper"
    },
    {
        "id": 2,
        "name": "Kim Daun"
    },
    {
        "id": 3,
        "name": "Sanli Maria"
    },
    {
        "id": 4,
        "name": "Clark Bruce"
    },
    {
        "id": 5,
        "name": "DePriest Abby"
    },
    {
        "id": 6,
        "name": "McMahon Thomass"
    },
    {
        "id": 7,
        "name": "Campos Frank"
    },
    {
        "id": 8,
        "name": "Rubel Max"
    },
    {
        "id": 9,
        "name": "Bubp Braydon"
    },
    {
        "id": 10,
        "name": "Ryan Tanay"
    },
]

def get_all_customers():
    return CUSTOMERS

# Function with a single parameter
def get_single_customer(id):
    # Variable to hold the found customers, if it exists
    requested_customer = None

    # Iterate the customerS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for customer in CUSTOMERS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if customer["id"] == id:
            requested_customer = customer

    return requested_customer

def create_customer(customer):
    # Get the id value of the last customer in the list
    max_id = CUSTOMERS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the customer dictionary
    customer["id"] = new_id

    # Add the customer dictionary to the list
    CUSTOMERS.append(customer)

    # Return the dictionary with `id` property added
    return customer

def delete_customer(id):
    # Initial -1 value for customer index, in case one isn't found
    customer_index = -1

    # Iterate the customerS list, but use enumerate() so that you
    # can access the index value of each item
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            # Found the customer. Store the current index.
            customer_index = index

    # If the customer was found, use pop(int) to remove it from list
    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)

def update_customer(id, new_customer):
    # Iterate the customerS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            # Found the customer. Update the value.
            new_customer["id"] = id
            CUSTOMERS[index] = new_customer
            break    
    else:
        create_customer(new_customer)  