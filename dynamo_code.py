import boto3

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
TABLE_NAME = 'Users'
table = dynamodb.Table(TABLE_NAME)

# Add a new user to DynamoDB
def add_user(first_name, last_name, favorite_genre):
    response = table.put_item(
        Item={
            'FirstName': first_name,
            'LastName': last_name,
            'FavoriteGenre': favorite_genre
        }
    )
    return response

# Get all users from DynamoDB
def get_all_users():
    response = table.scan()
    return response.get('Items', [])

# Update a user's favorite genre
def update_user_genre(first_name, last_name, new_genre):
    response = table.update_item(
        Key={
            'FirstName': first_name,
            'LastName': last_name
        },
        UpdateExpression='SET FavoriteGenre = :genre',
        ExpressionAttributeValues={
            ':genre': new_genre
        }
    )
    return response

# Delete a user from the table
def delete_user(first_name, last_name):
    response = table.delete_item(
        Key={
            'FirstName': first_name,
            'LastName': last_name
        }
    )
    return response