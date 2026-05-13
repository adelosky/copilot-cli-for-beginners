import json
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self) -> None:
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.books = []
            return
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []
            return

        if not isinstance(data, list):
            print("Warning: data.json must contain a list of books. Starting with empty collection.")
            self.books = []
            return

        loaded_books: List[Book] = []
        for index, record in enumerate(data, start=1):
            if not isinstance(record, dict):
                print(f"Warning: skipping invalid book record at position {index}.")
                continue

            title = record.get("title")
            author = record.get("author")
            year = record.get("year")
            read = record.get("read", False)

            if not isinstance(title, str) or not title.strip():
                print(f"Warning: skipping book record {index} with invalid title.")
                continue
            if not isinstance(author, str) or not author.strip():
                print(f"Warning: skipping book record {index} with invalid author.")
                continue
            if not isinstance(year, int) or year < 0:
                print(f"Warning: skipping book record {index} with invalid year.")
                continue
            if not isinstance(read, bool):
                print(f"Warning: skipping book record {index} with invalid read status.")
                continue

            loaded_books.append(
                Book(title=title.strip(), author=author.strip(), year=year, read=read)
            )

        self.books = loaded_books

    def save_books(self) -> None:
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        normalized_title = self._validate_non_empty_text(title, "Title")
        normalized_author = self._validate_non_empty_text(author, "Author")
        normalized_year = self._validate_year(year)

        book = Book(title=normalized_title, author=normalized_author, year=normalized_year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return list(self.books)

    def find_book_by_title(self, title: str) -> Optional[Book]:
        normalized_title = self._validate_non_empty_text(title, "Title")
        for book in self.books:
            if book.title.lower() == normalized_title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        normalized_author = self._validate_non_empty_text(author, "Author")
        return [b for b in self.books if b.author.lower() == normalized_author.lower()]

    @staticmethod
    def _validate_non_empty_text(value: str, field_name: str) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string.")

        normalized_value = value.strip()
        if not normalized_value:
            raise ValueError(f"{field_name} cannot be empty.")

        return normalized_value

    @staticmethod
    def _validate_year(year: int) -> int:
        if not isinstance(year, int):
            raise ValueError("Year must be an integer.")
        if year < 0:
            raise ValueError("Year cannot be negative.")
        return year
