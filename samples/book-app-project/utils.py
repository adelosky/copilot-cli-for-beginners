def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    choice = input("Choose an option (1-5): ").strip()
    if choice not in {"1", "2", "3", "4", "5"}:
        print("Invalid choice. Please enter a number between 1 and 5.")
        return ""
    return choice


def get_book_details() -> tuple[str, str, int]:
    title = input("Enter book title: ").strip()
    if not title:
        raise ValueError("Title cannot be empty.")

    author = input("Enter author: ").strip()
    if not author:
        raise ValueError("Author cannot be empty.")

    year_input = input("Enter publication year: ").strip()
    year = 0
    if year_input:
        try:
            year = int(year_input)
            if year < 0 or year > 9999:
                print("Year out of range. Defaulting to 0.")
                year = 0
        except ValueError:
            print(f"'{year_input}' is not a valid year. Defaulting to 0.")

    return title, author, year


def print_books(books: list) -> None:
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        try:
            status = "✅ Read" if book.read else "📖 Unread"
            print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
        except AttributeError as e:
            print(f"{index}. [Error displaying book: {e}]")
