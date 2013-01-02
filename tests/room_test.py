from scaffolding import Room, Object, \
                        Openable, Lightable, \
                        Bed, Dresser, Lamp

import unittest

class TestAdventure(unittest.TestCase):

    def setUp(self):
        self.dresser = Dresser()
        self.bed = Bed()
        self.lamp = Lamp()
        self.room = Room(name = "Room", objects = [self.dresser, self.bed, self.lamp], description = "A room.", exits = {})
    def tearDown(self):
        pass


    def test_room_defaults(self):
        "Defaults are being passes correctly"
        self.assertEquals(self.room.name, "Room")
        self.assertEquals(self.room.objects, [self.dresser, self.bed, self.lamp])
        self.assertEquals(self.room.description, "A room.")
        self.assertEquals(self.room.exits, {})
    def test_room_look(self):
        "room.look() returns room.description"
        self.assertEquals(self.room.look(), self.room.description)

if __name__ == "__main__":
    unittest.main()