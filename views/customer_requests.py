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