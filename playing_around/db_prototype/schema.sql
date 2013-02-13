drop table if exists users;
create table users (
  id integer primary key autoincrement
  );

drop table if exists actions;
create table actions (
  num integer primary key autoincrement,
  action string not null,
  user integer not null
  );

