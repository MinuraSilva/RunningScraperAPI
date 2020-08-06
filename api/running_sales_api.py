from flask import Flask
from flask_restx import Resource, Api
from werkzeug.middleware.proxy_fix import ProxyFix

from api.request_parsers import search_parser

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='RunningSalesAPI', description='Search the running sales database')

search_api = api.namespace('search', description='Search Running Sales')


@search_api.route('/')
class SearchParameters(Resource):

    @search_api.expect(search_parser)
    def get(self):
        args = search_parser.parse_args()
        print(args)
        return args


if __name__ == '__main__':
    app.run(debug=True)
