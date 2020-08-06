# Not needed since I used url query parameters.
# The code below can be used instead to get the search parameters through the request body.
# Note that this can only be used in a PUT/POST since GET does not accept a body.
# Remember to bind the model to the route with a decorator like so if using:

# @api.route('/someroute')
# class Search(Resource):
#    @api.marshal_with(search_request_model)
#    def post(self):



# absolute_range_query = api.model("Absolute Range Query", {
#     'gte': fields.Float(required=False, description="Minimum Dollar value", example=10),
#     'lte': fields.Float(required=False, description="Maximum Dollar value", example=100),
# })
#
# percentage_range_query = api.model("Percentage Range Query", {
#     'gte': fields.Float(required=False, description="Minimum percentage discount (as decimal)", example=0.10),
#     'lte': fields.Float(required=False, description="Maximum percentage discount (as decimal)", example=1.0),
# })
#
#
# # all of the string fields except for search_string and sort_by can be comma separated to pass in multiple values
# # multiple values always treated as an OR (even for colour)
# search_request_model = api.model('Search Request', {
#     'search_string': fields.String(required=True, description="A bunch of search terms"),
#
#     'brand': fields.List(fields.String(required=False),
#                          example=["adidas", "nike"],
#                          description="A list of brands"),
#     'item_type': fields.List(fields.String(required=False),
#                              example=["shirt", "shorts"],
#                              description="A list of clothing items"),
#     'size': fields.List(fields.String(required=False),
#                         example=["s", "m"],
#                         description="A list of sizes"),
#     'colour': fields.List(fields.String(required=False),
#                           example=["red", "blue"],
#                           description="A list of colours"),
#     'store': fields.List(fields.String(required=False),
#                          example=["adidas.ca", "mec.ca"],
#                          description="A list of store domains"),
#
#     'price_range': fields.Nested(absolute_range_query),
#     'discount_range': fields.Nested(percentage_range_query),
#     'absolute_discount_range': fields.Nested(absolute_range_query),
#
#     'sort_by': fields.String(required=True,
#                              default="_score",
#                              example='sale_price',
#                              enum=["_score", "sale_price", "original_price", "absolute_discount", "discount_percentage"],
#                              description="One of [_score, sale_price, original_price, absolute_discount,"
#                                          "discount_percentage]. _score is the elasticsearch relevance metric."),
# }, description="adafde")
