import sqlite3
from schemas.books import CompleteBook, PartialBook

class BookModel:
    conn = sqlite3.connect("books.db")

    @staticmethod
    def get_all() -> list[CompleteBook]:
        with BookModel.conn as conn:
            cursor = conn.cursor()
            query: str = """
            SELECT id, isbn, title
            FROM books
            """
            results: list[tuple[int, str, str]] = cursor.execute(query).fetchall()
        
        books = list(map(lambda result: CompleteBook(id=result[0], isbn=result[1], title=result[2]), results))
        return books
    
    @staticmethod
    def get_by_id(id: int) -> CompleteBook:
        with BookModel.conn as conn:
            cursor = conn.cursor()

            query: str = """
            SELECT id, isbn, title
            FROM books
            WHERE id = ?
            """
            results: list[tuple[int, str, str]] = cursor.execute(query, (id, )).fetchall()
        
        [book, *_] = list(map(lambda result: CompleteBook(id=result[0], isbn=result[1], title=result[2]), results))
        return book
    
    @staticmethod
    def get_by_isbn(isbn: str) -> list[CompleteBook]:
        with BookModel.conn as conn:
            cursor = conn.cursor()

            query: str = """
            SELECT id, isbn, title
            FROM books
            WHERE isbn = ?
            """

            results: list[tuple[int, str, str]] = cursor.execute(query, (isbn, )).fetchall()
        
        books = list(map(lambda result: CompleteBook(id=result[0], isbn=result[1], title=result[2]), results))
        return books
    
    @staticmethod
    def get_by_title(title: str) -> list[CompleteBook]:
        with BookModel.conn as conn:
            cursor = conn.cursor()

            query: str = """
            SELECT id, isbn, title 
            FROM books
            WHERE title = ?
            """
            results: list[tuple[int, str, str]] = cursor.execute(query, (title, )).fetchall()

        books = list(map(lambda result: CompleteBook(id=result[0], isbn=result[1], title=result[2]), results))    
        return books
    
    @staticmethod
    def create(book: PartialBook) -> CompleteBook:
        with BookModel.conn as conn:
            cursor = conn.cursor()
            id_query: str = """
            SELECT MAX(id)
            FROM books
            """

            [id, *_] = cursor.execute(id_query).fetchone()
            id += 1

            create_query: str = """
            INSERT INTO books
            VALUES (?, ?, ?)
            """

            cursor.execute(create_query, (id, book.isbn, book.title, ))
            conn.commit()

        new_book = BookModel.get_by_id(id)
        return new_book
    
    @staticmethod
    def update_title(id: int, title: str) -> CompleteBook:
        with BookModel.conn as conn:
            cursor = conn.cursor()

            query = """
            UPDATE books
            SET title = ?
            WHERE id = ?
            """

            cursor.execute(query, (title, id, ))
            conn.commit()

        updated_book = BookModel.get_by_id(id)
        return updated_book
    
    @staticmethod
    def delete(id: int) -> CompleteBook:
        with BookModel.conn as conn:
            cursor = conn.cursor()
            deleted_book = BookModel.get_by_id(id)
        
            translated_query = """
            DELETE FROM translated
            WHERE book_id = ?;
            """

            cursor.execute(translated_query, (id, ))
            conn.commit()

            book_query = """
            DELETE FROM books
            WHERE id = ?
            """

            cursor.execute(book_query, (id, ))
            conn.commit()

        return deleted_book