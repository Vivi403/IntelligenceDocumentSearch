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


def get_chunks_by_ids(chunk_ids):

    if not chunk_ids:
        return []

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                select id, document_id, content
                from chunks
                where id = any(%s)
                """,
                (chunk_ids,),
            )

            return cursor.fetchall()


def fulltext_search(user_input, limit):

    if not user_input:
        return []

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                id,
                document_id,
                content,
                ts_rank(
                    to_tsvector('russian', content),
                    plainto_tsquery('russian', %s)
                ) AS score
            FROM chunks
            WHERE to_tsvector('russian', content)
                @@ plainto_tsquery('russian', %s)
            ORDER BY score DESC
            LIMIT %s;
                """,
                (user_input, user_input, limit),
            )

            return cursor.fetchall()


def get_all_documents():

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                select id, filename, file_type, storage_path
                from documents
                order by id
                """)
            rows = cursor.fetchall()

    return [{"id": row[0], "filename": row[1], "file_type": row[2]} for row in rows]


def get_document_by_id(document_id):

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                select id, filename, file_type, storage_path
                from documents
                where id = %s
                """,
                (document_id,),
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "filename": row[1],
        "file_type": row[2],
        "storage_path": row[3],
    }


def delete_document(document_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                delete from documents
                where id = %s
                returning id
                """,
                (document_id,),
            )

            return cursor.fetchone()
