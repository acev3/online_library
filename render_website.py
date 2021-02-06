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
    with open('books_info.json') as f:
        books_info = json.load(f)
    os.makedirs("pages/", exist_ok=True)
    books_info = list(chunked(books_info, 10))
    pages = len(books_info)
    for i, chunked_books in enumerate(books_info, 1):
        books_data = list(chunked(chunked_books, 2))
        rendered_page = template.render(chunked_books=books_data, pages=pages, page=i)
        filename = "index{}.html".format(i)
        filepath = os.path.join("pages/", filename)
        with open(filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)


    """
    for chunked_books in books_info:
        books_data = list(chunked(chunked_books, 2))
        rendered_page = template.render(chunked_books=books_data)
        for i, books in enumerate(books_data, 1):
            filename = "index{}.html".format(i)
            filepath = os.path.join("pages/", filename)
            with open(filepath, 'w', encoding="utf8") as file:
                file.write(rendered_page)
    """


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')