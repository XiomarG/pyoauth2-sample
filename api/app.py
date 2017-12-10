from flask import Flask, request
from flask_restplus import Api, Resource, fields
import datetime, functools

app = Flask(__name__)
authorizations = {
    'apikey': {
        'type': 'apikey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(app,
          version='0.1',
          title='OAuth API',
          description='API interface for a sample oauth service',
          authorizations=authorizations
          )

healthCheckNS = api.namespace('healthCheck')


def auth_required(func):
    func = api.doc(security='apikey')(func)
    @functools.wraps(func)
    def check_auth(*args, **kwargs):
        if 'X-API-KEY' not in request.headers:
            api.abort('401', 'API key required')
        return func(*args, **kwargs)
    return check_auth


@healthCheckNS.route('', methods=['GET'])
@healthCheckNS.doc('health check')
@healthCheckNS.header('x-api-key', 'api key')
class HelloWorld(Resource):
    heathResponseModel = api.model('HeathCheck', {
        'status': fields.String(defaut='ok'),
        'now': fields.DateTime
    })

    @staticmethod
    @healthCheckNS.response(200, 'Success', heathResponseModel)
    def get():
        return {
            'status': 'ok',
            'now': datetime.datetime.now().replace(microsecond=0).isoformat()
        }


if __name__ == '__main__':
    app.run(debug=True)
