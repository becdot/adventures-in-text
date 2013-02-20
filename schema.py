from game import game
from scaffolding import VERBS

COLUMNS = []

def object_attributes(obj):
    attributes = {'room_id': 'NULL', 'subtype': obj.__class__.__name__}
    for attribute in dir(obj):
        if attribute in VERBS or attribute == 'look':
            continue
        elif attribute.startswith('__'):
            continue
        elif 'description' in attribute or attribute == 'name':
            continue
        elif getattr(obj, attribute).__class__.__name__ == 'instancemethod':
            continue
        elif getattr(obj, attribute).__class__.__name__ == 'Room':
            attributes[attribute] = getattr(obj, attribute).name
        else:
            attributes[attribute] = getattr(obj, attribute)
    return attributes

def column_names(*objects):
    return list(set(key for obj in objects for key in object_attributes(obj).keys()))

all_objects = [obj for room in game['rooms'] for obj in room.objects] + game['inv']
COLUMNS = list(column_names(*all_objects))

def set_rows(*objects):
    "Returns a list of dictionaries for each object, where the keys of each dictionary == column names of objects table"

    rows = []
    for obj in objects:
        attribute_dict = object_attributes(obj)
        for name in COLUMNS:
            if name not in attribute_dict:
                attribute_dict[name] = 'NULL'
        rows.append(attribute_dict)
    return rows

def create_database(*things):
    """['id', 'unique_name', 'room_id', 'subtype', 'objects', '_room', 'is_open', 'has_user', 'is_lit', 'block']"""

    user_info = """\
DROP TABLE if exists user_info;
CREATE TABLE user_info (
  game_id INTEGER PRIMARY KEY autoincrement,
  location TEXT
  );
"""

    rooms = """\
DROP TABLE if exists rooms;
CREATE TABLE rooms (
  id INTEGER PRIMARY KEY autoincrement,
  name TEXT,
  game_id INTEGER
  );
"""

    objects = """\
DROP TABLE if exists objects;
CREATE TABLE objects (
  id INTEGER PRIMARY KEY autoincrement,
"""

    for name in COLUMNS[:-1]:
        if name in ['unique_name', 'subtype', '_room']:
            objects += '  ' + name + ' TEXT,\n'
        else:
            objects += '  ' + name + ' INTEGER,\n'
    objects += '  ' + COLUMNS[-1] + ' INTEGER\n  );'

    return (user_info, rooms, objects)  