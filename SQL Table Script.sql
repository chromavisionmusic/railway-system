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

create table fare_chart
(train_no int(5) primary key,
2S float(5,2),
CC float(5,2),
EC float(6,2),
SL float(5,2),
3A float(5,2),
2A float(6,2),
1A float(6,2),
GEN float(5,2));

