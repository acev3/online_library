from livereload import Server, shell
import json
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import math


env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )


def on_reload(number_books_per_page=10, number_books_per_row=2):
    template = env.get_template('template.html')
    with open('media/books_info.json') as f:
        books = json.load(f)
    os.makedirs("pages/", exist_ok=True)
    chunked_books = list(chunked(books, number_books_per_page))
    pages = len(chunked_books)
    for i, book in enumerate(chunked_books, 1):
        double_chunked_books = list(chunked(book, number_books_per_row))
        rendered_page = template.render(chunked_books=double_chunked_books, pages=pages, current_page=i)
        filename = "index{}.html".format(i)
        filepath = os.path.join("pages/", filename)
        with open(filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')