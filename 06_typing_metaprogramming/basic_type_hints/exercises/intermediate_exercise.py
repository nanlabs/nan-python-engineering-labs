"""
Intermediate Exercise: Type Hints - Library Management System

OBJECTIVE:
Implementar un sistema básico para gestionar libros en una biblioteca
usando type hints para garantizar type safety.

REQUISITOS:
Implementar tres funciones con type hints completos:

1. add_book(title: str, author: str, year: int) -> Dict[str, str | int]
   - Crea un diccionario con la información del libro
   - Keys: "title", "author", "year"
   
2. search_books(books: List[Dict[str, str | int]], keyword: str) -> List[Dict[str, str | int]]
   - Busca libros donde el keyword aparezca en title o author (case-insensitive)
   - Retorna lista de libros que coincidan
   
3. get_books_by_year(books: List[Dict[str, str | int]], year: int) -> Optional[List[Dict[str, str | int]]]
   - Retorna libros publicados en un año específico
   - Retorna None si no hay libros de ese año
   - Retorna lista vacía si books está vacío

EJEMPLO DE USO:
>>> book1 = add_book("1984", "George Orwell", 1949)
>>> book2 = add_book("Animal Farm", "George Orwell", 1945)
>>> books = [book1, book2]
>>> search_books(books, "orwell")
[{'title': '1984', 'author': 'George Orwell', 'year': 1949}, 
 {'title': 'Animal Farm', 'author': 'George Orwell', 'year': 1945}]
"""

from typing import Dict, List, Optional


def add_book(title: str, author: str, year: int) -> Dict[str, str | int]:
    """
    Crea un diccionario representando un libro.
    
    Args:
        title: Título del libro
        author: Autor del libro
        year: Año de publicación
        
    Returns:
        Diccionario con keys "title", "author", "year"
    
    Examples:
        >>> add_book("1984", "George Orwell", 1949)
        {'title': '1984', 'author': 'George Orwell', 'year': 1949}
    """
    # TODO: Implementar
    # Retornar un diccionario con las tres keys
    pass


def search_books(
    books: List[Dict[str, str | int]], 
    keyword: str
) -> List[Dict[str, str | int]]:
    """
    Busca libros por palabra clave en título o autor.
    
    La búsqueda debe ser case-insensitive (ignorar mayúsculas/minúsculas).
    
    Args:
        books: Lista de diccionarios de libros
        keyword: Palabra a buscar en title o author
        
    Returns:
        Lista de libros que contengan el keyword en title o author
    
    Examples:
        >>> books = [
        ...     {'title': '1984', 'author': 'George Orwell', 'year': 1949},
        ...     {'title': 'Dune', 'author': 'Frank Herbert', 'year': 1965}
        ... ]
        >>> search_books(books, "orwell")
        [{'title': '1984', 'author': 'George Orwell', 'year': 1949}]
    """
    # TODO: Implementar
    # 1. Convertir keyword a lowercase
    # 2. Iterar sobre books
    # 3. Para cada book, verificar si keyword está en title.lower() o author.lower()
    # 4. Acumular los libros que coincidan en una lista
    # 5. Retornar la lista de resultados
    pass


def get_books_by_year(
    books: List[Dict[str, str | int]], 
    year: int
) -> Optional[List[Dict[str, str | int]]]:
    """
    Obtiene libros publicados en un año específico.
    
    Args:
        books: Lista de diccionarios de libros
        year: Año de publicación a filtrar
        
    Returns:
        Lista de libros del año especificado.
        None si no hay ningún libro de ese año.
        Lista vacía [] si books está vacío.
    
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
    # TODO: Implementar
    # 1. Si books está vacío, retornar []
    # 2. Filtrar books donde book["year"] == year
    # 3. Si hay resultados, retornar la lista
    # 4. Si no hay resultados, retornar None
    pass


if __name__ == "__main__":
    # Pruebas manuales - descomentar para probar tu implementación
    
    # # Crear libros
    # book1 = add_book("1984", "George Orwell", 1949)
    # book2 = add_book("Animal Farm", "George Orwell", 1945)
    # book3 = add_book("Dune", "Frank Herbert", 1965)
    # book4 = add_book("Foundation", "Isaac Asimov", 1951)
    # 
    # books = [book1, book2, book3, book4]
    # 
    # # Buscar por autor
    # print("Libros de Orwell:")
    # print(search_books(books, "orwell"))
    # 
    # # Buscar por título
    # print("\nLibros con 'Dune' en el título:")
    # print(search_books(books, "dune"))
    # 
    # # Buscar por año
    # print("\nLibros de 1949:")
    # print(get_books_by_year(books, 1949))
    # 
    # print("\nLibros de 2000:")
    # print(get_books_by_year(books, 2000))
    
    pass
