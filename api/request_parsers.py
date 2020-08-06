from flask_restx import reqparse
from api.enum_options import brand_options, item_type_options, size_options, colour_options, store_options, \
    sort_by_options
from api.parser_custom_datatypes import splitter, dollar_value, percentage_value
from flask_restx.inputs import boolean

search_parser = reqparse.RequestParser()
search_parser.add_argument('search_string', type=str,
                           help="String in search box", default=None, required=False)
search_parser.add_argument('brand', type=splitter("brand", brand_options),
                           help="Comma delimited list of brands", default=None, required=False)
search_parser.add_argument('item_type', type=splitter("item_type", item_type_options),
                           help="Comma delimited list of item_type", default=None, required=False)
search_parser.add_argument('size', type=splitter("size", size_options),
                           help="Comma delimited list of size", default=None, required=False)
search_parser.add_argument('colour', type=splitter("colour", colour_options),
                           help="Comma delimited list of colour", default=None, required=False)
search_parser.add_argument('store', type=splitter("store", store_options),
                           help="Comma delimited list of stores", default=None, required=False)

search_parser.add_argument('og_price_gte', type=dollar_value,
                           help="Minimum original price", default=None, required=False)
search_parser.add_argument('og_price_lte', type=dollar_value,
                           help="Maximum original price", default=None, required=False)
search_parser.add_argument('sale_price_gte', type=dollar_value,
                           help="Minimum sale price", default=None, required=False)
search_parser.add_argument('sale_price_lte', type=dollar_value,
                           help="Maximum sale price", default=None, required=False)
search_parser.add_argument('discount_gte', type=dollar_value,
                           help="Minimum discount dollar value", default=None, required=False)
search_parser.add_argument('discount_lte', type=dollar_value,
                           help="Maximum discount dollar value", default=None, required=False)
search_parser.add_argument('perc_dicount_gte', type=percentage_value,
                           help="Minimum percentage discount as decimal", default=None, required=False)
search_parser.add_argument('perc_dicount_lte', type=percentage_value,
                           help="Maximum percentage discount as decimal", default=None, required=False)

search_parser.add_argument('equivalent_other_geneder_size',
                           type=boolean,
                           help="Whether to search for equivalent sizes for other gender "
                                "(size conversion done automatically)",
                           default=False,
                           required=False)

search_parser.add_argument('sort_by',
                           choices=sort_by_options,
                           help="Sort results. _score is to sort by elasticsearch relevance",
                           default="_score",
                           required=False)



# Alternate method for dealing with enums that can accept a list (e.g. for brand)
# Difference is that multiple queries have to made instead of passing it in as a list
# http://localhost:5000/search/searchparam?brand=adidas&brand=nike
# Whereas the current way is simpler:
# http://localhost:5000/search/searchparam?brand=adidas,nike
# Example for alternative. Note the action="append" option.
# search_parser.add_argument('brand', type=str, action="append",
#                            choices=("adidas", "nike"),
#                            help="Brand. May provide multiple by passing in several ",
#                            default="adidas",
#                            required=False)
