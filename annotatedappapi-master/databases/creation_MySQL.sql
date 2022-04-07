create table annotations
(
    id bigint not null AUTO_INCREMENT,
    home varchar(255) not null,
    start timestamp not null,
    end timestamp not null,
    room varchar(255),
    activity_type varchar(255),
    status varchar(255) not null,
	constraint annotations_pk primary key (id)
);
