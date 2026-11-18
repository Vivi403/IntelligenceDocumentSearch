CREATE EXTENSION IF NOT EXISTS vector;
CREATE table documents(
    id bigserial primary key,
    filename text not null,
    file_type varchar(10) not null,
    storage_path text not null
);

create table chunks(
    id bigserial primary key,
    document_id BIGINT not null
        REFERENCES documents(id)
        on delete CASCADE,

    chunk_index INTEGER not null,
    content text not null,
    embedding vector(384) not null,

    unique(document_id, chunk_index)
);  

SELECT version();