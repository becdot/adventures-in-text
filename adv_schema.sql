DROP TABLE if exists user_info;
CREATE TABLE user_info (
  game_id INTEGER PRIMARY KEY autoincrement,
  location TEXT
  );

DROP TABLE if exists rooms;
CREATE TABLE rooms (
  id INTEGER PRIMARY KEY autoincrement,
  name TEXT,
  game_id INTEGER
  );

DROP TABLE if exists objects;
CREATE TABLE objects (
  id INTEGER PRIMARY KEY autoincrement,
  unique_name TEXT,
  room_id INTEGER,
  subtype TEXT,
  objects INTEGER,
  _room TEXT,
  is_open INTEGER,
  has_user INTEGER,
  is_lit INTEGER,
  block INTEGER
  );