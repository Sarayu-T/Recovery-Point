CREATE TABLE `lost_item`(
`ID` INT AUTO_INCREMENT NOT NULL,
`item_name` varchar(30) NOT NULL,
`category` varchar(30) NOT NULL,
`description` varchar(200) NOT NULL,
`location_lost` varchar(100) default null,
`datetime` datetime default null,
`item_image` varchar(100) default null,
PRIMARY KEY(`ID`)
);

CREATE TABLE `found_item`(
`ID` INT AUTO_INCREMENT NOT NULL,
`item_name` varchar(30) NOT NULL,
`category` varchar(30) NOT NULL,
`description` varchar(200) NOT NULL,
`location_found` varchar(100) default null,
`datetime` datetime default null,
`item_image` varchar(100) default null,
PRIMARY KEY(`ID`)
);