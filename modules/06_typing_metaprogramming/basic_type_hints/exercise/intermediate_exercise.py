"""
Intermediate Exercise: Type Hints - Library Management System

OBJECTIVE:
Implement a basic system to manage books in a library
using type hints to guarantee type safety.

REQUIREMENTS:
Implement three functions with complete type hints:

1. add_book(title: str, author: str, year: int) -> Dict[str, str | int]
   - Create a dictionary with the book information
   - Keys: "title", "author", "year"

2. search_books(books: List[Dict[str, str | int]], keyword: str) -> List[Dict[str, str | int]]
   - Search books where the keyword appears in title or author (case-insensitive)
   - Return a list of matching books

3. get_books_by_year(books: List[Dict[str, str | int]], year: int) -> Optional[List[Dict[str, str | int]]]
   - Return books published in a specific year
   - Return None if there are no books for that year
   - Return an empty list if books is empty

USAGE EXAMPLE:
>>> book1 = add_book("1984", "George Orwell", 1949)
>>> book2 = add_book("Animal Farm", "George Orwell", 1945)
>>> books = [book1, book2]
>>> search_books(books, "orwell")
[{'title': '1984', 'author': 'George Orwell', 'year': 1949},
 {'title': 'Animal Farm', 'author': 'George Orwell', 'year': 1945}]
"""


def add_book(title: str, author: str, year: int) -> dict[str, str | int]:
    """
    Create a dictionary representing a book.

    Args:
        title: Book title
        author: Book author
        year: Publication year

    Returns:
        Dictionary with keys "title", "author", "year"

    Examples:
        >>> add_book("1984", "George Orwell", 1949)
        {'title': '1984', 'author': 'George Orwell', 'year': 1949}
    """
    # TODO: Implement
    # Return a dictionary with the three keys
    pass


def search_books(books: list[dict[str, str | int]], keyword: str) -> list[dict[str, str | int]]:
    """
    Search books by keyword in title or author.

    The search must be case-insensitive.

    Args:
        books: List of book dictionaries
        keyword: Word to search in title or author

    Returns:
        List of books containing the keyword in title or author

    Examples:
        >>> books = [
        ...     {'title': '1984', 'author': 'George Orwell', 'year': 1949},
        ...     {'title': 'Dune', 'author': 'Frank Herbert', 'year': 1965}
        ... ]
        >>> search_books(books, "orwell")
        [{'title': '1984', 'author': 'George Orwell', 'year': 1949}]
    """
    # TODO: Implement
    # 1. Convert keyword to lowercase
    # 2. Iterate over books
    # 3. For each book, check whether keyword is in title.lower() or author.lower()
    # 4. Accumulate matching books in a list
    # 5. Return the result list
    pass


def get_books_by_year(
    books: list[dict[str, str | int]], year: int
) -> list[dict[str, str | int]] | None:
    """
    Get books published in a specific year.

    Args:
        books: List of book dictionaries
        year: Publication year to filter by

    Returns:
        List of books from the specified year.
        None if there are no books from that year.
        Empty list [] if books is empty.

    Examples:
        >>> books = [
        ...     {'title': '1984', 'author': 'George Orwell', 'year': 1949},
        ...     {'title': 'Dune', 'author': 'Frank Herbert', 'year': 1965},
        ...     {'title': 'Animal Farm', 'author': 'George Orwell', 'year': 1945}
        ... ]
        >>> get_books_by_year(books, 1949)
        [{'title': '1984', 'author': 'George Orwell', 'year': 1949}]
        >>> get_books_by_year(books, 2000)
        None
    """
    # TODO: Implement
    # 1. If books is empty, return []
    # 2. Filter books where book["year"] == year
    # 3. If there are results, return the list
    # 4. If there are no results, return None
    pass


if __name__ == "__main__":
    # Manual tests - uncomment to test your implementation

    # # Create books
    # book1 = add_book("1984", "George Orwell", 1949)
    # book2 = add_book("Animal Farm", "George Orwell", 1945)
    # book3 = add_book("Dune", "Frank Herbert", 1965)
    # book4 = add_book("Foundation", "Isaac Asimov", 1951)
    #
    # books = [book1, book2, book3, book4]
    #
    # # Search by author
    # print("Orwell books:")
    # print(search_books(books, "orwell"))
    #
    # # Search by title
    # print("\nBooks with 'Dune' in the title:")
    # print(search_books(books, "dune"))
    #
    # # Search by year
    # print("\nBooks from 1949:")
    # print(get_books_by_year(books, 1949))
    #
    # print("\nBooks from 2000:")
    # print(get_books_by_year(books, 2000))

    pass
