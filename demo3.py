import random
import datetime
import uuid

def generate_complex_data(data_type, constraints=None):
    """Generates complex data based on specified type and constraints."""

    if constraints is None:
        constraints = {}

    if data_type == "integer":
        min_val = constraints.get("min", -1000)
        max_val = constraints.get("max", 1000)
        return random.randint(min_val, max_val)

    elif data_type == "float":
        min_val = constraints.get("min", -1000.0)
        max_val = constraints.get("max", 1000.0)
        return random.uniform(min_val, max_val)

    elif data_type == "string":
        length = constraints.get("length", random.randint(5, 20))
        allowed_chars = constraints.get("chars", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        return "".join(random.choice(allowed_chars) for _ in range(length))

    elif data_type == "boolean":
        return random.choice([True, False])

    elif data_type == "date":
        start_date = constraints.get("start", datetime.date(2000, 1, 1))
        end_date = constraints.get("end", datetime.date(2024, 1, 1))
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        return start_date + datetime.timedelta(days=random_number_of_days)

    elif data_type == "uuid":
        return str(uuid.uuid4())

    elif data_type == "list":
        item_type = constraints.get("item_type", "integer")  # Default to integer if not specified
        length = constraints.get("length", random.randint(1, 10))
        item_constraints = constraints.get("item_constraints", {}) # Constraints for list items
        return [generate_complex_data(item_type, item_constraints) for _ in range(length)]

    elif data_type == "dict":
        fields = constraints.get("fields", {}) # Dictionary of field names and their types/constraints
        data = {}
        for field_name, field_constraints in fields.items():
            field_type = field_constraints.get("type", "string") # Default to string
            field_cons = field_constraints.get("constraints", {})
            data[field_name] = generate_complex_data(field_type, field_cons)
        return data

    else:
        return None  # Handle unknown data types


def generate_test_cases(num_cases, schema):
    """Generates test cases based on a schema."""
    test_cases = []

    for _ in range(num_cases):
        test_case = {}
        for field_name, field_constraints in schema.items():
            field_type = field_constraints.get("type", "string")  # Default to string if type not specified
            field_cons = field_constraints.get("constraints", {})
            test_case[field_name] = generate_complex_data(field_type, field_cons)
        test_cases.append(test_case)
    return test_cases


# Example usage with a complex schema:
schema = {
    "id": {"type": "uuid"},
    "name": {"type": "string", "constraints": {"length": 25}},
    "age": {"type": "integer", "constraints": {"min": 18, "max": 65}},
    "is_active": {"type": "boolean"},
    "created_at": {"type": "date", "constraints": {"start": datetime.date(2023, 1, 1)}},
    "price": {"type": "float", "constraints": {"min": 0.0, "max": 100.0}},
    "tags": {"type": "list", "constraints": {"item_type": "string", "length": 3, "item_constraints": {"length": 5}}},
    "address": {
        "type": "dict",
        "constraints": {
            "fields": {
                "street": {"type": "string"},
                "city": {"type": "string"},
                "zip": {"type": "string", "constraints": {"length": 5, "chars":"0123456789"}},
                "coordinates": {"type": "list", "constraints": {"item_type": "float", "length": 2}}
            }
        }
    }
}

test_data = generate_test_cases(5, schema)  # Generate 5 test cases
for case in test_data:
    print(case)



# Example of using the generated test data (you would adapt this to your model):
# for case in test_data:
#    model_output = your_model.predict(case)  # Replace your_model with your actual model
#    # ... evaluate model_output against expected results ...
