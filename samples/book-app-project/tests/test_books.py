import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False


def test_add_book_strips_whitespace():
    collection = BookCollection()
    book = collection.add_book("  1984  ", "  George Orwell  ", 1949)
    assert book.title == "1984"
    assert book.author == "George Orwell"


def test_add_book_rejects_empty_title():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Title cannot be empty."):
        collection.add_book("   ", "George Orwell", 1949)


def test_add_book_rejects_empty_author():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Author cannot be empty."):
        collection.add_book("1984", "   ", 1949)


def test_add_book_rejects_negative_year():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Year cannot be negative."):
        collection.add_book("1984", "George Orwell", -1)


def test_add_book_rejects_non_integer_year():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Year must be an integer."):
        collection.add_book("1984", "George Orwell", "1949")


def test_list_books_returns_copy():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    listed_books = collection.list_books()
    listed_books.clear()
    assert len(collection.books) == 1


def test_find_book_by_title_rejects_empty_title():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Title cannot be empty."):
        collection.find_book_by_title("   ")


def test_find_by_author_rejects_empty_author():
    collection = BookCollection()
    with pytest.raises(ValueError, match="Author cannot be empty."):
        collection.find_by_author("   ")


def test_find_by_author_returns_matching_books():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Animal Farm", "George Orwell", 1945)
    collection.add_book("Dune", "Frank Herbert", 1965)
    matches = collection.find_by_author("george orwell")
    assert [book.title for book in matches] == ["1984", "Animal Farm"]


def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_load_books_handles_corrupted_json(tmp_path, monkeypatch, capsys):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("{not valid json}", encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()

    assert collection.books == []
    captured = capsys.readouterr()
    assert "data.json is corrupted" in captured.out


def test_load_books_skips_malformed_records(tmp_path, monkeypatch, capsys):
    temp_file = tmp_path / "data.json"
    temp_file.write_text(
        """
[
  {"title": "1984", "author": "George Orwell", "year": 1949, "read": false},
  {"title": "", "author": "No Name", "year": 2000, "read": false},
  {"title": "Bad Read", "author": "Author", "year": 2001, "read": "yes"},
  {"title": "Bad Year", "author": "Author", "year": -1, "read": false}
]
""".strip(),
        encoding="utf-8",
    )
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()

    assert len(collection.books) == 1
    assert collection.books[0].title == "1984"
    captured = capsys.readouterr()
    assert "skipping book record" in captured.out


def test_save_books_persists_books(tmp_path, monkeypatch):
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))

    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)

    saved_data = temp_file.read_text(encoding="utf-8")
    assert '"title": "Dune"' in saved_data
    assert '"author": "Frank Herbert"' in saved_data
