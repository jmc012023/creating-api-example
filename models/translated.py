import sqlite3
from schemas.translated import CompleteTranslated

class TranslatedModel:
    conn = sqlite3.connect("books.db")

    @staticmethod
    def get_all():
        with TranslatedModel.conn as conn:
            cursor = conn.cursor()

            query: str = """
            SELECT b.id, b.title, t.name, t.id
            FROM books b
            JOIN translated td
                ON b.id = td.book_id
            JOIN translators t
                ON td.translator_id = t.id
            ORDER BY b.title;
            """
            results: list[tuple[int, str, str, int]] = cursor.execute(query).fetchall()
        
        translated = list(map(lambda result: CompleteTranslated(b_id=result[0], b_title=result[1], t_name=result[2], t_id=result[3]), results))
        return translated
    
    @staticmethod
    def get_by_title(title: str):
        with TranslatedModel.conn as conn:
            cursor = conn.cursor()

            query: str = """
            SELECT b.id, b.title, t.name, t.id
            FROM books b
            JOIN translated td
                ON b.id = td.book_id
            JOIN translators t
                ON td.translator_id = t.id
            WHERE b.title = ?
            ORDER BY b.title
            ;
            """
            results: list[tuple[int, str, str, int]] = cursor.execute(query, (title, )).fetchall()

        translated = list(map(lambda result: CompleteTranslated(b_id=result[0], b_title=result[1], t_name=result[2], t_id=result[3]), results))
        return translated
    
    @staticmethod
    def get_by_name(name: str):
        with TranslatedModel.conn as conn:
            cursor = conn.cursor()

            query: str = """
            SELECT b.id, b.title, t.name, t.id
            FROM books b
            JOIN translated td
                ON b.id = td.book_id
            JOIN translators t
                ON td.translator_id = t.id
            WHERE t.name = ?
            ORDER BY t.name
            ;
            """
            results: list[tuple[int, str, str, int]] = cursor.execute(query, (name, )).fetchall()

        translated = list(map(lambda result: CompleteTranslated(b_id=result[0], b_title=result[1], t_name=result[2], t_id=result[3]), results))
        return translated
    
    @staticmethod
    def create_translated(b_id: int, t_id: int):

        with TranslatedModel.conn as conn:
            cursor = conn.cursor()

            b_query: str = """
            SELECT "id"
            FROM books
            WHERE "id" = ?;
            """

            t_query: str = """
            SELECT "id"
            FROM translators
            WHERE "id" = ?;
            """    
            
            result_b: tuple[int,] | None = cursor.execute(b_query, (b_id, )).fetchone()
            result_t: tuple[int,] | None = cursor.execute(t_query, (t_id, )).fetchone()

            if (result_b != None) and (result_t != None):
                [resul_b_id, *_] = result_b
                [resul_t_id, *_] = result_t
            else:
                cursor.close()
                conn.close()
                return "mensaje invalido"
            
            insert_query = """
            INSERT INTO translated
            VALUES (?, ?);
            """
            conn.execute(insert_query, (resul_t_id, resul_b_id, ))
            conn.commit()

            result_query = """
            SELECT b.id, b.title, t.name, t.id
            FROM books b
            JOIN translated td
                ON b.id = td.book_id
            JOIN translators t
                ON td.translator_id = t.id
            WHERE b.id = ? AND t.id = ?
            """
            result_translated: tuple[int, str, str, int] = cursor.execute(result_query, (resul_b_id, resul_t_id, )).fetchone()

        new_translated = CompleteTranslated(b_id=result_translated[0], b_title=result_translated[1], t_name=result_translated[2], t_id=result_translated[3])        
        return new_translated
    
    @staticmethod
    def update_translator(b_id: int, t_id: int, new_id_t: int):

        with TranslatedModel.conn as conn:
            cursor = conn.cursor()

            update_query = """
            UPDATE translated
            SET translator_id = ?
            WHERE book_id = ? AND translator_id = ?;
            """

            cursor.execute(update_query, (new_id_t, b_id, t_id, ))
            conn.commit()

            result_query = """
            SELECT b.id, b.title, t.name, t.id
            FROM translated td
            JOIN books b
                ON td.book_id = b.id
            JOIN translators t
                ON td.translator_id = t.id
            WHERE td.book_id = ? AND td.translator_id = ?;
            """

            results = cursor.execute(result_query, (b_id, new_id_t, )).fetchall()

        updated_translated = list(map(lambda result: CompleteTranslated(b_id=result[0], b_title=result[1], t_name=result[2], t_id=result[3]), results))
        return updated_translated
    
    @staticmethod
    def update_book(t_id: int, b_id: int, new_b_id: int):

        with TranslatedModel.conn as conn:
            cursor = conn.cursor()

            update_query = """
            UPDATE translated
            SET book_id = ?
            WHERE translator_id = ? AND book_id = ?;
            """

            cursor.execute(update_query, (new_b_id, t_id, b_id, ))
            conn.commit()

            result_query = """
            SELECT b.id, b.title, t.name, t.id
            FROM translated td
            JOIN books b
                ON td.book_id = b.id
            JOIN translators t
                ON td.translator_id = t.id
            WHERE td.translator_id = ? AND td.book_id = ?;
            """

            results = cursor.execute(result_query, (t_id, new_b_id, )).fetchall()

        updated_translated = list(map(lambda result: CompleteTranslated(b_id=result[0], b_title=result[1], t_name=result[2], t_id=result[3]), results))
        return updated_translated
    
    @staticmethod
    def delete_by_book(b_id: int, t_id: int):
        with TranslatedModel.conn as conn:
            cursor = conn.cursor()

            result_query = """
            SELECT b.id, b.title, t.name, t.id
            FROM translated td
            JOIN books b
                ON td.book_id = b.id
            JOIN translators t
                ON td.translator_id = t.id
            WHERE td.translator_id = ? AND td.book_id = ?;
            """

            result = cursor.execute(result_query, (t_id, b_id, )).fetchone()
            delete_query = """
            DELETE FROM translated
            WHERE book_id = ? AND translator_id = ?;
            """

            cursor.execute(delete_query, (b_id, t_id, ))
            conn.commit()

        delete_translated = CompleteTranslated(b_id=result[0], b_title=result[1], t_name=result[2], t_id=result[3])
        return delete_translated