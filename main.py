import collections
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from pprint import pprint

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


def year_view(year: int):
    year_last_digit = str(year)[-1]
    if year_last_digit in ['2', '3', '4']:
        return f'{year} года'
    elif year_last_digit == '1':
        return f'{year} год'
    else:
        return f'{year} лет'


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

company_foundation_year = 1920
current_year = datetime.now().year

wines_df = pd.read_excel('wine2.xlsx', na_values='', keep_default_na=False).fillna('')
products_deserialized = collections.defaultdict(list)

for category in wines_df['Категория'].unique():
    products_deserialized[category] = wines_df.groupby(by='Категория').get_group(name=category).drop(['Категория'], axis=1).to_dict('records')

rendered_page = template.render(
    products=products_deserialized,
    company_age=year_view(current_year - company_foundation_year)
)

with open('template.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
