from datetime import timedelta, datetime
from ..config import aws_config

LOCK_ID = 'Locked'


def acquire():
    current_time = datetime.now()
    expiration_time = current_time + timedelta(minutes=300)

    print("Fetching current lock...")
    try:
        response = aws_config.lock_table.get_item(Key={'LockId': LOCK_ID})
        lock_item = response.get('Item')
    except Exception as e:
        print(f"Error fetching lock: {e}")
        return False

    print("Checking lock validity...")
    if lock_item:
        lock_expiration_time = datetime.fromisoformat(lock_item['ExpirationTime'])

        if current_time < lock_expiration_time:
            print("Lock is still valid, cannot acquire lock.")
            return False
        else:
            print("Lock has expired, attempting to acquire a new lock.")

    print("Acquiring lock...")
    try:
        aws_config.lock_table.put_item(
            Item={
                'LockId': LOCK_ID,
                'ExpirationTime': expiration_time.isoformat()
            },
            ConditionExpression='attribute_not_exists(LockId) OR ExpirationTime <= :current_time',
            ExpressionAttributeValues={':current_time': current_time.isoformat()}
        )
        print('Lock acquired or updated!')
        return True
    except aws_config.dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        print('Failed to acquire lock.')
        return False


def release():
    aws_config.lock_table.delete_item(Key={'LockId': LOCK_ID})
    print('Lock released!')
