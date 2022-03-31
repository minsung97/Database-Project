create database db_201611189;

use db_201611189;

create table User(
	userid int primary key,
    age int not null,
    gender char(2) not null,
    occupation varchar(20) not null,
    zipcode varchar(5) not null
);

create table Item(
	movieid int primary key,
    title varchar(100) not null,
    releasedate varchar(30) not null,
    v_releasedate varchar(30),
    url varchar(1000) not null,
    genre varchar(37) not null
);

create table Genre(
	genrename varchar(30),
    genrecode int primary key
);

create table Occupation(
	occupationname varchar(30) not null unique 
);

create table Data(
	userid int not null,
    movieid int not null,
    rating int not null,
    timestamp varchar(10) not null,
    primary key (userid,movieid),
    foreign key (userid) references User(userid),
    foreign key (movieid) references Item(movieid)
);

select *
from User;
select *
from Item;
select *
from Genre;
select *
from Occupation;
select *
from Data;