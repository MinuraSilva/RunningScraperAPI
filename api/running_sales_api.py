from flask import Flask
from flask_restx import Resource, Api
from werkzeug.middleware.proxy_fix import ProxyFix

from elasticsearch import Elasticsearch

import api.settings as settings
from api.request_parser.request_parsers import search_parser
from api.es_query_builder.search import run_query

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='RunningSalesAPI', description='Search the running sales database')

search_api = api.namespace('search', description='Search Running Sales')

# elasticsearch  connection
client = Elasticsearch(settings.es_hosts,
                       port=settings.es_port,
                       maxsize=settings.es_max_connections)


@search_api.route('/')
class SearchParameters(Resource):

    @search_api.expect(search_parser)
    def get(self):
        args = search_parser.parse_args()
        page_number = args["page_number"]
        sort_by = args["sort_by"]

        try:
            results = run_query(client,
                                args,
                                sort_by,
                                page_items=settings.num_results_per_page,
                                page_no=page_number)
        except Exception as e:
            results = {"exception during search": e}

        # print(args)
        # print(results)
        return results


if __name__ == '__main__':
    app.run(debug=True)
