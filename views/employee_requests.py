EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    },
    {
        "id": 2,
        "name": "Daun Kim"
    },
    {
        "id": 3,
        "name": "Maria Sanli"
    },
    {
        "id": 4,
        "name": "Bruce Clark"
    },
    {
        "id": 5,
        "name": "Abby DePriest"
    },
    {
        "id": 6,
        "name": "Thomass McMahon"
    },
    {
        "id": 7,
        "name": "Frank Campos"
    },
]

def get_all_employees():
    return EMPLOYEES

# Function with a single parameter
def get_single_employee(id):
    # Variable to hold the found employees, if it exists
    requested_employee = None

    # Iterate the employeeS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for employee in EMPLOYEES:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if employee["id"] == id:
            requested_employee = employee

    return requested_employee