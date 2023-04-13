from executor import execute

def lambda_handler(event, context):
    execute(event)

lambda_handler({}, {})