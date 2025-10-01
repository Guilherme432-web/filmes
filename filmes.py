import boto3
:dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',  # substitua pela sua região
    aws_access_key_id='SUA_ACCESS_KEY',
    aws_secret_access_key='SUA_SECRET_KEY'
)
table = dynamodb.Table('User  Profiles')

def get_user_profile(user_id):
    params = {
        'Key': {
            'PK': f'USER#{user_id}',
            'SK': 'PROFILE'
        }
    }
    response = table.get_item(**params)
    return response.get('Item')

def get_user_movie_ranking(user_id):
    params = {
        'KeyConditionExpression': 'PK = :pk and begins_with(SK, :skPrefix)',
        'ExpressionAttributeValues': {
            ':pk': f'USER#{user_id}',
            ':skPrefix': 'MOVIE#'
        }
    }
    response = table.query(**params)
    return response.get('Items', [])

# Configuração do DynamoDB (coloque suas credenciais aqui ou use variáveis de ambiente)
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',  # substitua pela sua região
    aws_access_key_id='SUA_ACCESS_KEY',
    aws_secret_access_key='SUA_SECRET_KEY'
)

table = dynamodb.Table('User   Profiles')

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
    params = {
        'Key': {
            'PK': f'USER#{user_id}',
            'SK': 'PROFILE'
        }
    }
    response = table.get_item(**params)
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
        return None  # Nada para atualizar

    update_expr = 'SET ' + ', '.join(update_expression)

    response = table.update_item(
        Key={
            'PK': f'USER#{user_id}',
            'SK': 'PROFILE'
        },
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    return response.get('Attributes')

def delete_user_profile(user_id):
    response = table.delete_item(
        Key={
            'PK': f'USER#{user_id}',
            'SK': 'PROFILE'
        }
    )
    return response
