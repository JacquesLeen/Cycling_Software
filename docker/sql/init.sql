create table if not exists dim_cyclists (
    cyclist_id int not null primary key,
    name varchar(250) not null,
    nationality varchar(250),
    age int,
    team_id int
);

create table if not exists dim_teams (
    team_id int not null primary key,
    name varchar(250) not null,
    nationality varchar(250)
);

create table if not exists public.dim_races (
    race_id int not null primary key,
    category varchar(250),
    country varchar(250),
    type varchar(250)
)