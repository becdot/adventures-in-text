from scaffolding import Room, Object, \
                        Openable, Lightable, \
                        Bed, Dresser, Lamp

import unittest

class TestRooms(unittest.TestCase):

    def setUp(self):
        self.dresser = Dresser()
        self.bed = Bed()
        self.lamp = Lamp()
        self.room = Room(name = "Room", objects = [self.dresser, self.bed, self.lamp], description = "A room.", exits={})
        
    def tearDown(self):
        pass


    def test_room_defaults(self):
        "Defaults are being passed correctly"
        self.assertEquals(self.room.name, "Room")
        self.assertEquals(self.room.objects, [self.dresser, self.bed, self.lamp])
        self.assertEquals(self.room.description, "A room.")
        self.assertEquals(self.room.exits, {})
    
    def test_room_look(self):
        "room.look() returns room.description"
        self.assertEquals(self.room.look(), self.room.description)

    def test_move_room(self):
        """Calling move should return the room object that is in that direction.  
        If the direction does not exist, an error should be thrown."""
        # existing direction
        other_room = Room(name='', objects=[], description='', exits={'north':self.room})
        self.room.exits['south'] = other_room
        self.assertEquals(self.room.move('south'), other_room)
        # direction that does not exist
        self.assertEquals(self.room.move('west'), "You cannot go that way.")

if __name__ == "__main__":
    unittest.main()