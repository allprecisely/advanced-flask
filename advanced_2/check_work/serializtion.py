## Serialization
# from marshmallow import Schema, fields
#
#
# class BookSchema(Schema):
#     title = fields.Str()
#     author = fields.Str()
#
#
# class Book:
#     def __init__(self, title, author, description):
#         self.title = title
#         self.author = author
#         self.description = description
#
#
# book = Book(1, '2', '3')
# book_schema = BookSchema()
#
# print(book_schema.dump(book))

## Deserialization
from marshmallow import Schema, fields


class BookSchema(Schema):
    title = fields.Str()
    author = fields.Str()


data = {'title': '1', 'author': '2'}

book_schema = BookSchema()
print(book_schema.load(data))
