import boto3
from werkzeug.security import generate_password_hash, check_password_hash

# DynamoDB connection (replace with your actual DynamoDB connection setup)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('users')  # Assuming a DynamoDB table named 'users'

def hash_password(password):
    """Hashes the provided password."""
    return generate_password_hash(password)

def create_user(username, password):
    """Creates a new user in the DynamoDB table if the username doesn't exist."""
    hashed_password = hash_password(password)
    
    # Check if the username already exists
    try:
        response = table.get_item(Key={'username': username})
        if 'Item' in response:
            return False  # Username exists already
    except Exception as e:
        print(f"Error checking user existence: {e}")
        return False

    # If the username doesn't exist, create a new user
    try:
        table.put_item(
            Item={'username': username, 'password': hashed_password}
        )
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def verify_user(username, password):
    """Verifies a user's login credentials."""
    try:
        # Fetch user by username
        response = table.get_item(Key={'username': username})
        if 'Item' not in response:
            return False  # Username doesn't exist

        # Check password
        stored_hash = response['Item']['password']
        return check_password_hash(stored_hash, password)
    except Exception as e:
        print(f"Error verifying user: {e}")
        return False