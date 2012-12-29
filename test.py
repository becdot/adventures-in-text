from adventure import Room, Object, User

import unittest

class FakeObject:
    def __init__(self, location=None, name=''):
        self.location = location
        self.name = name

class TestAdventure(unittest.TestCase):

    def test_room_defaults(self):
        "Defaults are passed in correctly to the Room class"
        obj = FakeObject()
        room = Room(exits={'north': 'northern room'}, objects=[obj], name='room', description='a room')
        self.assertEquals(room.exits, {'north': 'northern room'})
        self.assertEquals(room.objects, [obj])
        self.assertEquals(room.name, 'room')
        self.assertEquals(room.description, 'a room')

    def test_setting_object_location(self):
        "When objects are passed to the Room init function, they are assigned that room as their location"
        couch = FakeObject()
        chair = FakeObject()
        room = Room(objects=[couch, chair])
        self.assertEquals(couch.location, room)
        self.assertEquals(chair.location, room)

if __name__ == "__main__":
    unittest.main()