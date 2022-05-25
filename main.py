import collections

from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


COMPANY_FOUNDATION_YEAR = 1920


def year_view(year: int):
    year_last_digit = str(year)[-1]
    if year_last_digit in ['2', '3', '4']:
        return f'{year} года'
    elif year_last_digit == '1':
        return f'{year} год'
    else:
        return f'{year} лет'


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    current_year = datetime.now().year

    wines_df = pd.read_excel('products.xlsx', na_values='', keep_default_na=False).fillna('')
    products_by_category = wines_df.groupby(by='Категория')

    products_deserialized = collections.defaultdict(list)

    for category in wines_df['Категория'].unique():
        products_deserialized[category] = products_by_category.get_group(name=category)
        products_deserialized[category] = products_deserialized[category].drop(['Категория'], axis=1).to_dict('records')

    rendered_page = template.render(
        products=products_deserialized,
        company_age=year_view(current_year - COMPANY_FOUNDATION_YEAR)
    )

    with open('template.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
