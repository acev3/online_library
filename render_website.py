from livereload import Server, shell
import json
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )


def on_reload():
    template = env.get_template('template.html')
    with open('books_info.json') as f:
        books_info = json.load(f)
    books_info = list(chunked(books_info, 2))
    rendered_page = template.render(chunked_books=books_info)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')