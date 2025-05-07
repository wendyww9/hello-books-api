from app.routes.route_utilities import validate_model, create_model, get_models_with_filters
from werkzeug.exceptions import HTTPException
from app.models.book import Book
from app.models.author import Author
import pytest

def test_validate_model(two_saved_books):
    # Act
    result_book = validate_model(Book, 1)

    # Assert
    assert result_book.id == 1
    assert result_book.title == "Ocean Book"
    assert result_book.description == "watr 4evr"

def test_validate_model_missing_record(two_saved_books):
    # Act & Assert
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_book = validate_model(Book, "3")
    
def test_validate_model_invalid_id(two_saved_books):
    # Act & Assert
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_book = validate_model(Book, "cat")

# We use the `client` fixture because we need an
# application context to work with the database session
def test_create_model_book(client):
    # Arrange
    test_data = {
        "title": "New Book",
        "description": "The Best!"
    }

    # Act
    data, status_code = create_model(Book, test_data)

    # Assert
    assert status_code == 201
    assert data == {
        "id": 1,
        "title": "New Book",
        "description": "The Best!"
    }

def test_create_model_book_missing_data(client):
    # Arrange
    test_data = {
        "description": "The Best!"
    }

    # Act & Assert
    # Calling `create_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException) as error:
        result_book = create_model(Book, test_data)

    response = error.value.response
    assert response.status == "400 BAD REQUEST"

def test_create_model_author(client):
    # Arrange
    test_data = {
        "name": "New Author"
    }

    # Act
    data, status_code = create_model(Author, test_data)

    # Assert
    assert status_code == 201
    assert data == {
        "id": 1,
        "name": "New Author"
    }

def test_get_models_with_filters_one_matching_book(two_saved_books):
    # Act
    result = get_models_with_filters(Book, {"title": "ocean"})

    # Assert
    assert result == [{
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }]