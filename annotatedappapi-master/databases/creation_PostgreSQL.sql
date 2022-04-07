-- Ce script cree les tables de la base de donnees d'annotations

-- On cree le schema et on assigne le search_path
CREATE SCHEMA IF NOT EXISTS annotations;
SET search_path TO annotations;

drop table annotations;
create table annotations
(
    id            bigint    not null constraint annotations_pk primary key,
    home          varchar   not null,
    start         timestamp not null,
    "end"         timestamp not null,
    room          varchar,
    activity_type varchar,
    status        varchar not null
);

