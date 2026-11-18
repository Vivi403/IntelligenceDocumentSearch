from src.db.connection import get_connection
from pgvector.psycopg import register_vector


def save_document(filename, file_type, storage_path):

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                            insert into documents(filename, file_type, storage_path)
                            values(%s, %s, %s)
                            returning id
                            """,
                (filename, file_type, storage_path),
            )

            rows = cursor.fetchone()

    return rows[0]


def save_chunks(document_id, chunks, embeddings):

    if len(chunks) != len(embeddings):
        raise ValueError("Чанков и векторов должно быть одинаковое количество")

    if any(len(embedding) != 384 for embedding in embeddings):
        raise ValueError("Размерность embedding должна быть равна 384")

    with get_connection() as conn:
        register_vector(conn)

        chunk_ids = []

        with conn.cursor() as cursor:
            for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

                cursor.execute(
                    """
                    insert into chunks(document_id, chunk_index, content, embedding)
                    values(%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (document_id, index, chunk, embedding),
                )

                chunk_ids.append(cursor.fetchone()[0])

    return chunk_ids
