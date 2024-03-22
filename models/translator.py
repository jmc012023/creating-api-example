import sqlite3
from schemas.translators import CompleteTranslator, PartialTranslator

class TranslatorModel:
    conn = sqlite3.connect("books.db")

    @staticmethod
    def get_all() -> list[CompleteTranslator]:
        with TranslatorModel.conn as conn:
            cursor = conn.cursor()

            query: str = """
            SELECT id, name
            FROM translators
            """
            results: list[tuple[int, str]] = cursor.execute(query).fetchall()
            
        translators = list(map(lambda result: CompleteTranslator(id=result[0], name=result[1]), results))  
        return translators
    
    @staticmethod
    def get_by_id(id: int) -> CompleteTranslator:
        with TranslatorModel.conn as conn:
            cursor = conn.cursor()

            query: str = """
            SELECT id, name
            FROM translators
            WHERE id = ?
            """
            results: list[tuple[int, str]] = cursor.execute(query, (id, )).fetchall()

        [translator, *_] = list(map(lambda result: CompleteTranslator(id=result[0], name=result[1]), results))    
        return translator
    
    @staticmethod
    def get_by_name(name: str) -> list[CompleteTranslator]:
        with TranslatorModel.conn as conn:
            cursor = conn.cursor()

            query: str = """
            SELECT id, name
            FROM translators
            WHERE name = ?
            """
            results: list[tuple[int, str]] = cursor.execute(query, (name, )).fetchall()

        translators = list(map(lambda result: CompleteTranslator(id=result[0], name=result[1]), results))
        return translators

    @staticmethod
    def create(translator: PartialTranslator):
        with TranslatorModel.conn as conn:
            cursor = conn.cursor()
            id_query: str = """
            SELECT MAX(id)
            FROM translators
            """

            [id, *_] = cursor.execute(id_query).fetchone()
            id += 1

            create_query: str = """
            INSERT INTO translators
            VALUES (?, ?)
            """
            cursor.execute(create_query, (id, translator.name, ))
            conn.commit()

        new_translator = TranslatorModel.get_by_id(id) # CompleteTranslator(id=id, name=translator.name)
        return new_translator
    
    @staticmethod
    def update(translator: CompleteTranslator) -> CompleteTranslator:
        with TranslatorModel.conn as conn:
            cursor = conn.cursor()

            query = """
            UPDATE translators
            SET name = ?
            WHERE id = ?
            """

            cursor.execute(query, (translator.name, translator.id, ))
            conn.commit()

        updated_translator = TranslatorModel.get_by_id(translator.id)
        return updated_translator
    
    @staticmethod
    def delete(id: int) -> CompleteTranslator:
        with TranslatorModel.conn as conn:
            cursor = conn.cursor()

            deleted_translator = TranslatorModel.get_by_id(id)

            translated_query = """
            DELETE FROM translated
            WHERE translator_id = ?;
            """

            cursor.execute(translated_query, (id, ))
            conn.commit()

            translator_query = """
            DELETE FROM translators
            WHERE id = ?
            """

            cursor.execute(translator_query, (id, ))
            conn.commit()

        return deleted_translator