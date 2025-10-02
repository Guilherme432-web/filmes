import boto3
import os
from botocore.exceptions import ClientError


dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
)

TABLE_NAME = 'User_Profiles'
table = dynamodb.Table(TABLE_NAME)

def create_table_if_not_exists():
    try:
        dynamodb.meta.client.describe_table(TableName=TABLE_NAME)
        print(f"✅ Tabela '{TABLE_NAME}' já existe.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f" Criando tabela '{TABLE_NAME}'...")
            table = dynamodb.create_table(
                TableName=TABLE_NAME,
                KeySchema=[
                    {'AttributeName': 'PK', 'KeyType': 'HASH'},
                    {'AttributeName': 'SK', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'PK', 'AttributeType': 'S'},
                    {'AttributeName': 'SK', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            table.wait_until_exists()
            print(f"✅ Tabela '{TABLE_NAME}' criada com sucesso!")
        else:
            raise
        
def create_user_profile(user_id, nome, idade):
    item = {
        'PK': f'USER#{user_id}',
        'SK': 'PROFILE',
        'nome': nome,
        'idade': idade
    }
    table.put_item(Item=item)
    return item

def get_user_profile(user_id):
    response = table.get_item(
        Key={
            'PK': f'USER#{user_id}',
            'SK': 'PROFILE'
        }
    )
    return response.get('Item')

def update_user_profile(user_id, nome=None, idade=None):
    update_expression = []
    expression_attribute_values = {}

    if nome is not None:
        update_expression.append('nome = :n')
        expression_attribute_values[':n'] = nome
    if idade is not None:
        update_expression.append('idade = :i')
        expression_attribute_values[':i'] = idade

    if not update_expression:
        return None

    response = table.update_item(
        Key={
            'PK': f'USER#{user_id}',
            'SK': 'PROFILE'
        },
        UpdateExpression='SET ' + ', '.join(update_expression),
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    return response.get('Attributes')

def delete_user_profile(user_id):
    table.delete_item(
        Key={
            'PK': f'USER#{user_id}',
            'SK': 'PROFILE'
        }
    )
