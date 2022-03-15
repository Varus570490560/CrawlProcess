-- auto-generated definition
create table remove_duplication
(
    id     int auto_increment
        primary key,
    sha256 varchar(32) not null,
    constraint remove_duplication_sha256_uindex
        unique (sha256)
);