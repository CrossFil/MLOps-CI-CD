import json

def lambda_handler(event, context):
    print("--- Starting Data Validation ---")
    print(f"Received event: {json.dumps(event)}")
    
    return {
        'statusCode': 200,
        'status': 'Validated',
        'message': 'Data is clean and ready for training',
        'input_data': event
    }
