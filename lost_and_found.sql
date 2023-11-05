create table if not exists ticket(
`ticket_id` int auto_increment not null,
 `name` varchar(30),
`subject` varchar(100) not null,
`issue` varchar(300) not null,
primary key(`ticket_id`)
);