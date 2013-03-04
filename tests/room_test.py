from scaffolding import Room, Object
from properties import Openable, Lightable
from objects import Bed, Dresser, Lamp, Chair
                        

import unittest

class TestRooms(unittest.TestCase):

    def setUp(self):
        self.dresser = Dresser()
        self.bed = Bed()
        self.lamp = Lamp()
        self.chair = Chair()
        self.room = Room(name = "Room", objects = [self.dresser, self.bed, self.lamp], description = "A room.", exits={})
        self.southern_room = Room(name='', objects=[], description='', exits={'north':self.room})
        self.room.exits['south'] = self.southern_room

    def tearDown(self):
        pass


    def test_room_defaults(self):
        "Defaults are being passed correctly"
        self.assertEquals(self.room.name, "Room")
        self.assertEquals(self.room.objects, [self.dresser, self.bed, self.lamp])
        self.assertEquals(self.room.description, "A room.")
        self.assertEquals(self.room.exits, {'south': self.southern_room})
    
    def test_room_look(self):
        "room.look() returns room.description"
        self.assertEquals(self.room.look(), self.room.description)

    def test_move_room(self):
        """Calling move should return the room object that is in that direction.  
        If the direction does not exist, an error should be thrown."""
        # existing direction
        self.assertEquals(self.room.move('south', []), self.southern_room)
        # direction that does not exist
        self.assertEquals(self.room.move('west', []), "You cannot go that way.")

    def test_move_when_standing(self):
        "User should not be able to move locations when standing on something"
        # when chair is in user's inventory
        inv = [self.chair]
        self.chair.has_user = True
        self.assertEquals(self.room.move('south', inv), "You must climb down first.")
        # when chair is in the room
        self.room.objects.append(self.chair)
        self.assertEquals(self.room.move('south', []), "You must climb down first.")
        # but should succeed when the user gets down
        self.chair.has_user = False
        self.assertEquals(self.room.move('south', []), self.southern_room)

    def test_equality(self):
        "Two rooms should be considered equal if they have the same name, description, objects, and exits"
        name, desc, exits = self.room.name, self.room.description, self.room.exits
        objs = [Dresser(), Lamp(), Bed()]
        other_room = Room(name, objs, desc, exits)
        # equal
        self.assertTrue(self.room == other_room)
        other_room.objects.pop()
        # not equal
        self.assertFalse(self.room == other_room)






if __name__ == "__main__":
    unittest.main()