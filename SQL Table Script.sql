create database railway_system;

use railway_system;

create table user_details
(username varchar(20) primary key,
name varchar(30) not null,
age int(2) not null,
gender char(1) not null,
aadhaar bigint(12) unique,
phone bigint(10) not null unique,
email varchar(50));

create table login_details
(username varchar(20) primary key,
password varchar(16) not null);

create table train_details
(train_no int(5) primary key,
train_name varchar(40) not null unique,
category varchar(15) not null,
source varchar(4) not null,
destination varchar(4) not null);

create table bookings
(PNR bigint(10) primary key,
train_no int(5) not null,
class varchar(2),
board_at varchar(4),
destination varchar(4),
NOP int(1),
booking_date date,
journey_date date,
fare float(7,2) not null);

