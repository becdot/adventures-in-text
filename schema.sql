drop table if exists actions;
create table actions (
  hash integer primary key autoincrement,
  action string not null
  );