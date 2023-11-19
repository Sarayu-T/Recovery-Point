-- LOST AND FOUND SYSTEM MySQL Tables

-- User details table
CREATE TABLE users (
`user_id` int auto_increment not null,
`name` varchar(30) not null,
`email` varchar(50) not null,
`password` varchar(128) not null,        
`phone_no` varchar(10) not null unique, 
primary key(`user_id`)
);

-- Ticket table
create table ticket (
`ticket_id` int auto_increment not null,
`user_id` INT NOT NULL default 0,
`name` varchar(30),
`subject` varchar(100) not null,
`issue` varchar(300) not null,
primary key(`ticket_id`),
FOREIGN KEY (`user_id`) references `users`(`user_id`) on update cascade on delete cascade
);

-- Lost Item details table
CREATE TABLE lost_item (
`ID` INT AUTO_INCREMENT NOT NULL,
`user_id` INT NOT NULL default 0,
`item_name` varchar(30) NOT NULL,
`category` varchar(30) NOT NULL,
`description` varchar(200) NOT NULL,
`location_lost` varchar(100) NOT null,
`datetime` datetime default null,
`item_image` varchar(100) default null,
PRIMARY KEY(`ID`),
FOREIGN KEY (`user_id`) references `users`(`user_id`) on update cascade on delete cascade
);

-- Found item details table
CREATE TABLE found_item (
`ID` INT AUTO_INCREMENT NOT NULL,
`user_id` INT NOT NULL default 0,
`item_name` varchar(30) NOT NULL,
`category` varchar(30) NOT NULL,
`description` varchar(200) NOT NULL,
`location_found` varchar(100) NOT null,
`datetime` datetime default null,
`item_image` varchar(100) default null,
PRIMARY KEY(`ID`),
FOREIGN KEY (`user_id`) references `users`(`user_id`) on update cascade on delete cascade
);

-- To display all users, lost items and found items
select * from users;
select * from lost_item;
select * from found_item;
select * from ticket;

-- To view all Lost and Found Items by a particular user
SELECT * FROM lost_item WHERE user_id = 1 UNION ALL SELECT * FROM found_item WHERE user_id = 1;

--  Retrieving specific Found Item columns for a user
SELECT ID, user_id, item_name, category, description, location_found FROM found_item WHERE user_id = 1;


--  Retrieving specific Lost Item columns for a user
SELECT ID, user_id, item_name, category, description, location_lost FROM lost_item WHERE user_id = 1;


-- Deleting a particular user and their corresponding Lost and/or Found Item details get deleted
DELETE FROM users WHERE user_id = 1;


-- To delete all details of the Lost and Found System
use trial;
ALTER TABLE lost_item DROP FOREIGN KEY `lost_item_ibfk_1`;
ALTER TABLE found_item DROP FOREIGN KEY `found_item_ibfk_1`;
ALTER TABLE ticket DROP FOREIGN KEY `ticket_ibfk_1`;
drop table users;
drop table ticket;
drop table lost_item;
drop table found_item;


-- If you want to add manual tuples (update the user_id each time)
-- So here, Susan has lost 2 items and found 2 items
INSERT INTO users (user_id, name, email, password, phone_no) 
VALUES (1, 'Susan', 'yeahsusan@gmail.com', 'YeahNope', '1234567890');

INSERT INTO lost_item (user_id, item_name, category, description, location_lost) 
VALUES (1, 'Lost Phone', 'Gadgets', 'Black iPhone', 'Class 407');
INSERT INTO lost_item (item_name, category, description, location_lost) 
VALUES (1, 'Lost Wallet', 'Bags/Wallets', 'Brown leather wallet', 'Library');
 
INSERT INTO found_item (item_name, category, description, location_found) 
VALUES (1, 'Lost Wallet', 'Bags/Wallets', 'Brown leather wallet', 'Library');
INSERT INTO found_item (item_name, category, description, location_found) 
VALUES (1, 'Lost Wallet', 'Bags/Wallets', 'Brown leather wallet', 'Library');
