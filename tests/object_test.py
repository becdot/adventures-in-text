from scaffolding import Object
from properties import Openable, Lightable, UnreachableLight, Gettable, Climbable, Container
from objects import Bed, Dresser, Lamp, UnreachableLamp, Chair

import unittest

class FakeObject:
    def __init__(self, name):
        self.name = name

class Room:
    def __init__(self, *objs):
        self.objects = [o for o in objs]

class TestObjects(unittest.TestCase):

    def setUp(self):
        self.dresser = Dresser()
        self.bed = Bed()
        self.lamp = Lamp()
        self.unreachable_lamp = UnreachableLamp()
        self.chair = Chair()

    def tearDown(self):
        pass

    # test bed
    def test_bed_description(self):
        "bed.description returns the description"
        self.bed.description = "A self.bed."
        self.assertEquals(self.bed.description, "A self.bed.")
    def test_bed_look(self):
        "bed.look() returns the item description"
        self.bed.description = "A self.bed."
        self.assertEquals(self.bed.look(), "A self.bed.")
    def test_bed_stand(self):
        "bed.stand() returns the specified message"
        # TODO make this so it is not hard-coded
        self.assertEquals(self.bed.stand(), "Didn't your mother teach you anything?")
    def test_bed_climb_equals_stand(self):
        "bed.climb() returns the same result as bed.stand()"
        self.assertEquals(self.bed.climb(), self.bed.stand())

    # test dresser
    def test_dresser_starts_closed(self):
        "dresser.is_open defaults to false"
        self.assertFalse(self.dresser.is_open)
    def test_closed_dresser_description(self):
        "dresser returns the description + closed_description when it is closed."
        self.assertEquals(str(self.dresser), self.dresser.description + '  ' + self.dresser.closed_description)
    def test_open_dresser_description(self):
        """dresser returns the description + open_description + a list of containing objects when self.objects is not empty
            and returns the description + open_description only when self.objects is empty"""
        # self.objects = []
        self.dresser.is_open = True
        self.assertEquals(str(self.dresser),\
        self.dresser.description + '  ' + self.dresser.open_description + '  This object is empty.')
        # self.objects = ["key"]
        key = FakeObject('key')
        self.dresser.objects = [key]
        self.assertEquals(str(self.dresser),\
            self.dresser.description + '  ' + self.dresser.open_description + '  ' + "This object has a key inside.")
        # self.objects = ["sword", "key"]
        sword = FakeObject('sword')
        self.dresser.objects = [sword, key]
        self.assertEquals(str(self.dresser),\
            self.dresser.description + '  ' + self.dresser.open_description + '  ' + "This object contains: sword, key.")
    def test_dresser_look(self):
        "dresser.look() returns the dresser.description + open/closed description (based on dresser.is_open)"
        self.assertEquals(self.dresser.look(), str(self.dresser))
        self.dresser.is_open = True
        self.assertEquals(self.dresser.look(), str(self.dresser))
    def test_open_dresser(self):
        """Opening a closed dresser sets dresser.is_open to True and returns dresser.open_description
            Opening an already open dresser returns a message"""
        # dresser is closed
        self.assertEquals(self.dresser.open(), self.dresser.open_description)
        self.assertTrue(self.dresser.is_open)
        # dresser is already open
        self.assertEquals(self.dresser.open(), "That object is as open as it can get!")
        self.assertTrue(self.dresser.is_open)
    def test_close_dresser(self):
        """Closing an open dresser sets dresser.is_open to False and returns dresser.closed_description
            Closing an already closed dresser returns a message"""
        # dresser is open
        self.dresser.is_open = True
        self.assertEquals(self.dresser.close(), self.dresser.closed_description)
        self.assertFalse(self.dresser.is_open)
        # dresser is already closed
        self.assertEquals(self.dresser.close(), "That object can't get any more closed.")
        self.assertFalse(self.dresser.is_open)
    # test container aspect of dresser
    def test_get_fails_when_object_is_closed(self):
        "Trying to get an object from a closed dresser should return an error message"
        room = Room(self.bed, self.dresser)
        self.dresser.objects.append(self.chair)
        inv = []
        self.assertEquals(self.chair.get(inventory=inv, location=room), "The object is closed.")
    def test_get_object_from_open_dresser(self):
        """Trying to get an object from an open dresser should add the object to the user's inventory 
        and remove it from the container"""
        room = Room(self.bed, self.dresser)
        self.dresser.objects.append(self.chair)
        inv = []
        self.dresser.open()
        self.chair.get(inventory=inv, location=room)
        self.assertEquals(self.dresser.objects, [])
        self.assertEquals(inv, [self.chair])
    def test_put_object_in_dresser(self):
        "Put in should put an item in the dresser only when it is open, and return an error message otherwise"
        room = Room(self.bed, self.dresser)
        inv = [self.chair]
        # dresser is closed
        self.assertEquals(self.dresser.put_in(self.chair, inventory=inv), "Try opening the container first.")
        # dresser is open
        self.dresser.open()
        self.dresser.put_in(self.chair, inventory=inv)
        self.assertEquals(self.dresser.objects, [self.chair])
        self.assertEquals(inv, [])
    def test_look_in_dresser(self):
        "Look_in should return the list of contained objects if the dresser is open, and an error otherwise"
        # self.is_open = False
        self.assertEquals(self.dresser.look_in(), "You cannot look inside a closed object.")
        # self.objects = []
        self.dresser.is_open = True
        self.assertEquals(self.dresser.look_in(), "This object is empty.")
        # self.objects = ["key"]
        key = FakeObject('key')
        self.dresser.objects = [key]
        self.assertEquals(self.dresser.look_in(), "This object has a key inside.")
        # self.objects = ["sword", "letter", "key"]
        sword = FakeObject('sword')
        self.dresser.objects = [sword, key]
        self.assertEquals(self.dresser.look_in(), "This object contains: sword, key.")


    # test lamp
    def test_lamp_starts_off(self):
        "lamp.is_lit defaults to false"
        self.assertFalse(self.lamp.is_lit)
    def test_lamp_descriptions(self):
        """lamp returns the description + off_description when lamp.is_lit is False
         and description + on_description when lamp.is_lit is True"""
        # off description
        self.assertEquals(str(self.lamp), self.lamp.description + '  ' + self.lamp.off_description)
        # on description
        self.lamp.is_lit = True
        self.assertEquals(str(self.lamp), self.lamp.description + '  ' + self.lamp.on_description)
    def test_lamp_look(self):
        "lamp.look() returns the lamp.description + on/off description (based on lamp.is_lit)"
        self.assertEquals(self.lamp.look(), str(self.lamp))
        self.lamp.is_lit = True
        self.assertEquals(self.lamp.look(), str(self.lamp))
    def test_light_lamp(self):
        """Lighting a lamp that is off sets lamp.is_lit to True and returns lamp.on_description
            Lighting an already lit lamp returns a message"""
        # lamp is lit
        self.assertEquals(self.lamp.light(), self.lamp.on_description)
        self.assertTrue(self.lamp.is_lit)
        # lamp is already light
        self.assertEquals(self.lamp.light(), "The object is already glowing brightly")
        self.assertTrue(self.lamp.is_lit)
    def test_snuff_lamp(self):
        """Snuffing a lit lamp sets lamp.is_lit to False and returns lamp.off_description
            Snuffing a lamp that is already off returns a message"""
        # lamp is lit
        self.lamp.is_lit = True
        self.assertEquals(self.lamp.snuff(), "The glow fades into blackness.")
        self.assertFalse(self.lamp.is_lit)
        # lamp is off
        self.assertEquals(self.lamp.snuff(), "The object cannot get any darker.")
        self.assertFalse(self.lamp.is_lit)

    # test unreachable lamp
    def test_unreachable_lamp_starts_off(self):
        "unreachable_lamp.is_lit defaults to false"
        self.assertFalse(self.unreachable_lamp.is_lit)
    def test_unreachable_lamp_descriptions(self):
        """unreachable_lamp returns the description + off_description when lamp.is_lit is False
         and description + on_description when lamp.is_lit is True"""
        # off description
        self.assertEquals(str(self.unreachable_lamp), self.unreachable_lamp.description + '  ' + self.unreachable_lamp.off_description)
        # on description
        self.unreachable_lamp.is_lit = True
        self.assertEquals(str(self.unreachable_lamp), self.unreachable_lamp.description + '  ' + self.unreachable_lamp.on_description)
    def test_unreachable_lamp_look(self):
        "unreachable_lamp.look() returns the unreachable_lamp.description + on/off description (based on unreachable_lamp.is_lit)"
        self.assertEquals(self.unreachable_lamp.look(), str(self.unreachable_lamp))
        self.unreachable_lamp.is_lit = True
        self.assertEquals(self.unreachable_lamp.look(), str(self.unreachable_lamp))
    def test_error_message_when_user_is_not_standing(self):
        "Trying to perform an action on the unreachable lamp returns an error message if the user is not standing on something."
        room = Room(self.unreachable_lamp)
        # unreachable_lamp is off
        self.assertEquals(self.unreachable_lamp.light(location=room), self.unreachable_lamp.error_description)
        self.assertFalse(self.unreachable_lamp.is_lit)
        # unreachable_lamp is lit
        self.unreachable_lamp.is_lit = True
        self.assertEquals(self.unreachable_lamp.snuff(location=room), self.unreachable_lamp.error_description)
        self.assertTrue(self.unreachable_lamp.is_lit)
    def test_light_unreachable_lamp(self):
        """User can light an unreachable lamp if standing on something."""
        room = Room(self.bed, self.chair)
        self.unreachable_lamp._room = room
        self.chair.has_user = True
        # unreachable_lamp is lit
        self.assertEquals(self.unreachable_lamp.light(location=room), self.unreachable_lamp.on_description)
        self.assertTrue(self.unreachable_lamp.is_lit)
        # unreachable_lamp is already lit
        self.assertEquals(self.unreachable_lamp.light(location=room), "The object is already glowing brightly")
        self.assertTrue(self.unreachable_lamp.is_lit)
    def test_snuff_unreachable_lamp(self):
        """User can snuff an unreachable lamp if standing on something."""
        # unreachable_lamp is lit
        room = Room(self.bed, self.chair)
        self.unreachable_lamp._room = room
        self.chair.has_user = True
        self.unreachable_lamp.is_lit = True
        self.assertEquals(self.unreachable_lamp.snuff(location=room), "The glow fades into blackness.")
        self.assertFalse(self.unreachable_lamp.is_lit)
        # unreachable_lamp is off
        self.assertEquals(self.unreachable_lamp.snuff(location=room), "The object cannot get any darker.")
        self.assertFalse(self.unreachable_lamp.is_lit)

    # test chair climability
    def test_chair_starts_off(self):
        "chair.has_user defaults to false"
        self.assertFalse(self.chair.has_user)
    def test_chair_look(self):
        "chair.look() returns the chair.description"
        self.assertEquals(self.chair.look(), str(self.chair))
    def test_climbing_chair(self):
        """Climbing a chair that does not already have a user standing on it sets has_user to True
            Otherwise, climbing sets has_user to False (climb is multipurpose)."""
        # chair is unoccupied
        inv = []
        self.assertEquals(self.chair.climb(inventory=inv), "You clamber onto the object.")
        self.assertTrue(self.chair.has_user)
        self.assertEquals(self.chair.climb(inventory=inv), "You step carefully back down.")
        self.assertFalse(self.chair.has_user)
    def test_get_on_and_off_chair(self):
        "Get_on and get_off are single-purpose (i.e. a user cannot use get_on to get off an object)"
        inv = []
        self.assertEquals(self.chair.get_off(inventory=inv), "You are not standing on anything.")
        self.assertFalse(self.chair.has_user)
        self.assertEquals(self.chair.get_on(inventory=inv), "You clamber onto the object.")
        self.assertTrue(self.chair.has_user)
        self.assertEquals(self.chair.get_on(inventory=inv), "You are already standing on that object!")
        self.assertTrue(self.chair.has_user)
        self.assertEquals(self.chair.get_off(inventory=inv), "You step carefully back down.")
        self.assertFalse(self.chair.has_user)
    def test_climb_when_chair_in_inventory(self):
        "User can only climb when the object is not in their inventory"
        inv = [self.chair]
        self.assertEquals(self.chair.climb(inventory=inv), 'You cannot climb that while still holding it.')
        inv = []
        self.assertEquals(self.chair.climb(inventory=inv), 'You clamber onto the object.')

    # test chair getability
    def test_get_chair(self):
        "Getting an object removes it from room.objects and adds it to the passed-in inventory"
        inv = []
        room = Room(self.chair, self.bed)
        self.chair.get(location=room, inventory=inv)
        self.assertEquals(room.objects, [self.bed])
        self.assertEquals(inv, [self.chair])
    def test_getting_object_not_in_room_objects_returns_error_message(self):
        """Getting an object that is already in user's inventory returns an error message, as does
            trying to get an object that does not exist."""
        inv = [self.chair]
        room = Room(self.bed)
        self.assertEquals(self.chair.get(location=room, inventory=inv), "You already have that object.")
        inv = []
        self.assertEquals(self.chair.get(location=room, inventory=inv), "That object does not exist.")
    def test_drop_chair(self):
        "Dropping an item removes it from user's inventory and places it in room.objects"
        inv = [self.chair]
        room = Room(self.bed)
        self.chair.drop(inventory=inv, location=room)
        self.assertEquals(inv, [])
        self.assertEquals(room.objects, [self.bed, self.chair])
    def test_drop_item_not_in_inventory(self):
        "Trying to drop an item that is not currently in the user's inventory returns an error message"
        inv = []
        room = Room(self.bed)
        self.assertEquals(self.chair.drop(location=room, inventory=inv), "That item is not currently in your inventory.")
        room.objects.append(self.chair)
        self.assertEquals(self.chair.drop(location=room, inventory=inv), "That item is not currently in your inventory.")


    # test equality
    def test_object_equality(self):
        new_chair = Chair()
        self.assertEquals(new_chair, self.chair)

    # test inequality
    def test_inequality(self):
        new_chair = Chair()
        new_chair.has_user = True
        self.assertNotEqual(new_chair, self.chair)

    # test openable
    def test_openable_synonyms(self):
        "Calling dresser.pull = dresser.open; dresser.shut and dresser.push = dresser.close"
        pull_if_closed = self.dresser.pull()
        self.dresser.is_open = False
        open_if_closed = self.dresser.open()
        self.assertEquals(pull_if_closed, open_if_closed)
        self.dresser.is_open = False
        self.assertEquals(self.dresser.shut(), self.dresser.close())
        self.assertEquals(self.dresser.push(), self.dresser.close())

    # test lightable
    def test_lightable_synonyms(self):
        "Calling lamp.turn_on = lamp.light; lamp.turn_off = lamp.snuff"
        turn_on_if_off = self.lamp.turn_on()
        self.lamp.is_lit = False
        light_if_off = self.lamp.light()
        self.assertEquals(turn_on_if_off, light_if_off)
        self.lamp.is_lit = False
        self.assertEquals(self.lamp.turn_off(), self.lamp.snuff())

    # test gettable 
    def test_gettable_synonyms(self):
        "Calling chair.pickup = chair.get"
        inv = []
        room = Room(self.chair, self.bed)
        self.chair.pickup(location=room, inventory=inv)
        self.assertEquals(room.objects, [self.bed])

    # test climbable
    def test_climbable_synonyms(self):
        "Calling chair.stand/get_on/get_off/get_down calls chair.climb"
        # stand is multipurpose (i.e. can be used to both get on and get off a climbable object)
        inv = []
        self.chair.stand(inventory=inv)
        self.assertTrue(self.chair.has_user)
        self.chair.stand(inventory=inv)
        self.assertFalse(self.chair.has_user)
        # get_on, get_off, and get_down are single purpose
        self.chair.get_on(inventory=inv)
        self.assertTrue(self.chair.has_user)
        self.chair.get_off(inventory=inv)
        self.assertFalse(self.chair.has_user)
        self.chair.get_down(inventory=inv)
        self.assertFalse(self.chair.has_user)

if __name__ == "__main__":
    unittest.main()