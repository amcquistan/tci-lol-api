
import os
import uuid

import boto3
from boto3.dynamodb.conditions import Key

from flask import request, jsonify
from flask_lambda import FlaskLambda

REGION = os.environ['REGION_NAME']
TABLE_NAME = os.environ['TABLE_NAME']

app = FlaskLambda(__name__)

dynamodb = boto3.resource('dynamodb', region_name=REGION)

def db_table(table_name=TABLE_NAME):
    return dynamodb.Table(table_name)


def parse_user_id(req):
    '''When frontend is built and integrated with an AWS Cognito
       this will parse and decode token to get user identification'''
    return req.headers['Authorization'].split()[1]


@app.route('/lists')
def fetch_lists():
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    tbl_response = db_table().query(KeyConditionExpression=Key('userId').eq(user_id))
    return jsonify(tbl_response['Items'])


@app.route('/lists', methods=('POST',))
def create_list():
    list_id = str(uuid.uuid4())
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    list_data = request.get_json()
    list_data.update(userId=user_id, listId=list_id)
    tbl = db_table()
    tbl.put_item(Item=list_data)
    tbl_response = tbl.get_item(Key={'userId': user_id, 'listId': list_id})
    return jsonify(tbl_response['Item']), 201


@app.route('/lists/<string:list_id>')
def fetch_list(list_id):
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    tbl_response = db_table().get_item(Key={'userId': user_id, 'listId': list_id})
    return jsonify(tbl_response['Item'])


@app.route('/lists/<string:list_id>', methods=('PUT',))
def update_list(list_id):
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    list_data = {k: {'Value': v, 'Action': 'PUT'}
                for k, v in request.get_json().items()}
    tbl_response = db_table().update_item(Key={'userId': user_id, 'listId': list_id},
                                          AttributeUpdates=list_data)
    return jsonify()


@app.route('/lists/<string:list_id>', methods=('DELETE',))
def delete_list(list_id):
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    db_table().delete_item(Key={'userId': user_id, 'listId': list_id})
    return jsonify()
