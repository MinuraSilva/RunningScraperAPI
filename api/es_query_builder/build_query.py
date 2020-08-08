from elasticsearch_dsl import Q

# Note: only have other gender conversion for shoes since clothing is too hard to convert.
# need to add gender equivalent shoe sizes in elasticsearch database and gender fields:
# gender: ["female', 'male']
# mens_size: 's'
# womens_size: 'm'
# the size for the opposite gender must be calculated and added at index time

# If search does not ask for opposite gender, add a gender filter in the search
# If  search asks for equivalent opposite gender, simply search for the mens/womens size without filtering by gender

# also add in parsing for unisex items which will have both men's and women's size in the availability xhr.
# e.g. https://www.adidas.ca/en/ultraboost-19-shoes/EF1344.html


def query_builder(**kw):
    # kw short for kwargs

    must = []
    should = []
    must_not = []
    _filter = []

    if kw["search_string"] is not None:
        search_box = Q("simple_query_string", query=kw["search_string"], fields=["*"])
        must.append(search_box)
    if kw["brand"] is not None:
        brand_filters = brand_filter(kw["brand"])
        _filter.append(brand_filters)  # important; must use append since single object
    if kw["item_type"] is not None:
        item_type = Q("multi_match",
                      query=kw["item_type"],
                      fields=[
                          "search_page.item_type",
                          "item_page.category_tags",
                          "item_page.description",
                          "item_page.sub_title"
                      ],
                      operator="OR")
        _filter.append(item_type)
    if kw["size"] is not None:
        size_filters = size_filter(kw["size"])
        _filter.append(size_filters)
    if kw["colour"] is not None:
        colour_filters = colour_filter(kw["colour"])
        _filter.append(colour_filters)
    if kw["store"] is not None:
        store_filters = store_filter(kw["store"])
        _filter.append(store_filters)
    if kw["og_price_gte"] is not None:
        og_price_gte = Q("range", item_page__original_price={"gte": kw["og_price_gte"]})
        _filter.append(og_price_gte)
    if kw["og_price_lte"] is not None:
        og_price_lte = Q("range", item_page__original_price={"lte": kw["og_price_lte"]})
        _filter.append(og_price_lte)
    if kw["sale_price_gte"] is not None:
        sale_price_gte = Q("range", item_page__sale_price={"gte": kw["sale_price_gte"]})
        _filter.append(sale_price_gte)
    if kw["sale_price_lte"] is not None:
        sale_price_lte = Q("range", item_page__sale_price={"lte": kw["sale_price_lte"]})
        _filter.append(sale_price_lte)
    if kw["discount_gte"] is not None:
        discount_gte = Q("range", item_page__absolute_discount={"gte": kw["discount_gte"]})
        _filter.append(discount_gte)
    if kw["discount_lte"] is not None:
        discount_lte = Q("range", item_page__absolute_discount={"lte": kw["discount_lte"]})
        _filter.append(discount_lte)
    if kw["perc_dicount_gte"] is not None:
        sale_perc_gte = Q("range", item_page__sale_percentage={"gte": kw["perc_dicount_gte"]})
        _filter.append(sale_perc_gte)
    if kw["perc_dicount_lte"] is not None:
        sale_perc_lte = Q("range", item_page__sale_percentage={"lte": kw["perc_dicount_lte"]})
        _filter.append(sale_perc_lte)
    if kw["equivalent_other_gender_shoe_size"]:
        # Need to first change the schema in the scraper so that the list of available sizes for the itemm's gender is
        # separated from the opposite gender sizes
        pass

    es_query = Q('bool',
                 must=[Q("match", search_page__brand="adidas")],
                 should=should,
                 must_not=must_not,
                 filter=_filter)

    return es_query


def brand_filter(brand_list):

    Q_list = []

    for brand in brand_list:
        Q_list.append(Q("match", search_page__brand=brand))

    or_query = Q('bool', should=Q_list)

    return or_query


def size_filter(size_list):
    Q_list = []

    for size in size_list:
        Q_list.append(Q("match", availability_page__available_sizes=size))

    or_query = Q('bool', should=Q_list)

    return or_query


def colour_filter(colour_list):
    Q_list = []

    for colour in colour_list:
        Q_list.append(Q("match", item_page__colour=colour))

    or_query = Q('bool', should=Q_list)

    return or_query


def store_filter(store_list):
    Q_list = []

    for store in store_list:
        Q_list.append(Q("wildcard", search_page__domain=f"*{store}*"))

    or_query = Q('bool', should=Q_list)

    return or_query
