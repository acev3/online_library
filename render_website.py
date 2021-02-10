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


def on_reload():
    template = env.get_template('template.html')
    with open('media/books_info.json') as f:
        books = json.load(f)
    os.makedirs("pages/", exist_ok=True)
    books = list(chunked(books, 10))
    pages = len(books)
    for i, book in enumerate(books, 1):
        chunked_books = list(chunked(books, 2))
        rendered_page = template.render(chunked_books=chunked_books, pages=pages, current_page=i)
        filename = "index{}.html".format(i)
        filepath = os.path.join("pages/", filename)
        with open(filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')