from adventure import Room, Object, User, build_description

import unittest

# class FakeObject:
#     def __init__(self, location=None, name=''):
#         self.location = location
#         self.name = name

# class FakeRoom:
#     def __init__(self, exits={}, objects=[], name='', description=''):
#         self.exits = exits
#         self.objects = objects
#         self.name = name
#         self.description = description

class TestAdventure(unittest.TestCase):

    # def test_room_defaults(self):
    #     "Defaults are passed in correctly to the Room class"
    #     obj = Object()
    #     room = Room(exits={'north': 'northern room'}, objects=[obj], name='room', base_description='a room')

    #     self.assertEquals(room.exits, {'north': 'northern room'})
    #     self.assertEquals(room.objects, [obj])
    #     self.assertEquals(room.name, 'room')
    #     self.assertEquals(room.description, 'a room')

    # def test_setting_object_location_room(self):
    #     "When objects are passed to the Room init function, they are assigned that room as their location"
    #     couch = Object()
    #     chair = Object()
    #     room = Room(objects=[couch, chair])

    #     self.assertEquals(couch.location, room)
    #     self.assertEquals(room.objects[0].location, room)

    #     self.assertEquals(chair.location, room)
    #     self.assertEquals(room.objects[1].location, room)

    # def test_setting_object_location_user(self):
    #     "When objects are passed to the User init function, they are assigned that user as their location"
    #     couch = Object()
    #     chair = Object()
    #     user = User(inventory=[couch, chair])

    #     self.assertEquals(couch.location, user)
    #     self.assertEquals(user.inventory[0].location, user)

    #     self.assertEquals(chair.location, user)
    #     self.assertEquals(user.inventory[1].location, user)

    # def test_move_object_from_room_to_user_inventory(self):
    #     "Room -> user: object.move removes the object from room.objects and adds it to user.inventory"
    #     penny = Object()
    #     dime = Object()
    #     room = Room(objects=[penny, dime])
    #     user = User(location=room)
    #     penny.move(user)

    #     self.assertEquals(room.objects, [dime])
    #     self.assertEquals(user.inventory, [penny])

    # def test_move_object_from_user_inventory_to_room(self):
    #     "User -> room: object.move removes the object from user.inventory and adds it to room.objects"
    #     coin = Object()
    #     room = Room()
    #     user = User(location=room, inventory=[coin])
    #     coin.move(user)

    #     self.assertEquals(room.objects, [coin])
    #     self.assertEquals(user.inventory, [])

    # def test_build_description_of_room_pos(self):
    #     "Additional description clause appears when the object is in room.objects"
    #     coin = Object(name='coin') # object must be named
    #     room = Room(objects=[coin])
    #     room.description = build_description(base='A room.', coin='A coin sits at the center.')
    #     self.assertEquals(room.description, "A room.  A coin sits at the center.")

    def test_build_description_of_room_neg(self):
        "Additional description clause does not appear when the object is not in room.objects"
        coin = Object(name='coin') # object must be named
        buffalo = Object(name='buffalo') # object must be named
        base = 'A room.'
        kwargs = {'buffalo': 'With a buffalo!', 'coin': 'A coin sits at the center.'}
        room = Room(objects=[coin], base_description=base, **kwargs)
        self.assertEquals(room.description, "A room.  A coin sits at the center.")


if __name__ == "__main__":
    unittest.main()