from flask import Blueprint, abort, make_response, request, Response
# from app.models.book import books
from app.models.book import Book
from ..db import db
from .route_utilities import create_model,validate_model, get_models_with_filters

bp = Blueprint("book_bp", __name__, url_prefix = "/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book, request_body)

@bp.get("")
def get_all_books():
    return get_models_with_filters(Book, request.args)
    

@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)
    return book.to_dict()


@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book,book_id)
    request_body = request.get_json()

    book.title = request_body['title']
    book.description = request_body['description']
    book.author = request_body['author']
    book.author_id = request_body['author_id']
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# @books_bp.get("")
# def get_all_books():
#     books_response = []
#     for book in books:
#         books_response.append(
#             {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description
#             }
#         )
#     return books_response

# @books_bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_book(book_id)

#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description,
#     }

# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         response = {"message": f"book {book_id} invalid"}
#         abort(make_response(response, 400))

#     for book in books:
#         if book.id == book_id:
#             return book

#     response = {"message": f"book {book_id} not found"}
#     abort(make_response(response, 404))
