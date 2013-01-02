# to-do - Pickupable property

from scaffolding import Room, Object, User, \
                        Openable, Lightable, \
                        Bed, Dresser, Lamp

import unittest

class TestUser(unittest.TestCase):

    def setUp(self):
        self.dresser = Dresser()
        self.bed = Bed()
        self.lamp = Lamp()
        self.room = Room(name = "Room", objects = [self.dresser, self.bed, self.lamp], description = "A room.", exits = {})
        self.user = User(name = "User", inventory = [], location = self.room)
    def tearDown(self):
        pass


    def test_user_defaults(self):
        "Defaults are being passed correctly"
        self.assertEquals(self.user.name, "User")
        self.assertEquals(self.user.inventory, [])
        self.assertEquals(self.user.location, self.room)
        
    def test_user_get(self):
        "user.get(object) puts the object in the user's inventory and removes it from room.objects"
        self.user.get(self.bed)
        self.assertEquals(self.user.inventory, [self.bed])
        self.assertEquals(self.room.objects, [self.dresser, self.lamp])
        self.user.get(self.lamp)
        self.assertEquals(self.user.inventory, [self.bed, self.lamp])
        self.assertEquals(self.room.objects, [self.dresser])
        
    def test_user_get_error_if_obj_in_inventory(self):
        "Error messages are returned if the user tries to get an object that is already in their inventory"
        self.user.get(self.bed)
        self.assertEquals(self.user.get(self.bed), "You already have that object.")
        
    def test_user_get_error_if_obj_does_not_exist(self):
        "Error messages are returned if the user tries to get an object that does not exist"
        # TODO make it so that the user can try to get uninitialized variables?
        self.assertEquals(self.user.get('chair'), "That object does not exist.")


if __name__ == "__main__":
    unittest.main()