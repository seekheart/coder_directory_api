from flask_restful_swagger_2 import Schema

class UserModel(Schema):
    type = 'object'
    properties = {
        '_id': {
            'type': 'integer',
            'format': 'int64'
        },
        'languages': {
            'type': 'array'
        }
    }