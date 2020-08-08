from math import floor

from elasticsearch_dsl import Search

from .build_query import query_builder


def run_query(es_connection, query_args, sort_by, page_no=0, page_items=40):
    # ES query must be built using the 'Q' shortcut from elasticsearch_dsl or be otherwise compatible and have a query
    # method that can be called

    es_query = query_builder(**query_args)

    start = page_items * page_no
    end = page_items * (page_no + 1)

    sort_by = sort_fieldname(sort_by)

    search = Search(using=es_connection, index="adidas_ca_items_2")[start:end]
    response = search.query(es_query).sort(sort_by).execute()
    total_num_results = response.hits.total.value

    last_page = floor(total_num_results / page_items)

    if (page_no > last_page) and page_no > 0:
        results = {"error": f"The requested page '{page_no}' exceeds the last page of results. "
                            f"Please try a number less than or equal to '{last_page}'",
                   "total_results": total_num_results,
                   "last_page": last_page}
    else:
        results = extract_results(response)
        results = {"total_results": total_num_results,
                   "last_page": last_page,
                   "results": results}

    return results


def extract_results(response):
    # extract just the results from the AttrDict as plain python dicts
    results = response.hits.hits

    results_list = [result["_source"].to_dict() for result in results]

    return results_list


def sort_fieldname(sort_option):
    #sort_by_options = ("_score", "sale_price", "original_price", "absolute_discount", "discount_percentage")
    field_name = {"_score": "_score",
                  "sale_price_asc":             "item_page.sale_price",
                  "sale_price_desc":            "-item_page.sale_price",
                  "original_price_asc":         "item_page.original_price",
                  "original_price_desc":        "-item_page.original_price",
                  "absolute_discount_asc":      "item_page.absolute_discount",
                  "absolute_discount_desc":     "-item_page.absolute_discount",
                  "discount_percentage_asc":    "item_page.sale_percentage",
                  "discount_percentage_desc":   "-item_page.sale_percentage"
                  }

    return field_name[sort_option]
