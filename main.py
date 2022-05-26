import collections

from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


COMPANY_FOUNDATION_YEAR = 1920
PRODUCTS_CATALOG_FILE = 'products.xlsx'


def year_view(year: int):
    year_last_digit = str(year)[-1]
    if year_last_digit in ['2', '3', '4']:
        return f'{year} года'
    elif year_last_digit == '1':
        return f'{year} год'
    else:
        return f'{year} лет'


def get_products_list_by_category(excel_catalogue_path: str) -> collections.defaultdict[list]:
    products_df = pd.read_excel(excel_catalogue_path, na_values=None, keep_default_na=False).to_dict('records')
    grouped_products = collections.defaultdict(list)

    for product in products_df:
        grouped_products[product['Категория']].append(product)

    return grouped_products


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    current_year = datetime.now().year

    products_deserialized = get_products_list_by_category(PRODUCTS_CATALOG_FILE)

    rendered_page = template.render(
        products=products_deserialized,
        company_age=year_view(current_year - COMPANY_FOUNDATION_YEAR)
    )

    with open('template.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
