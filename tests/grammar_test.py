from grammar import parse
from objects import Dresser, Bed, Lamp, Chair, UnreachableLamp
from scaffolding import Room
import unittest
from copy import deepcopy

class TestGrammar(unittest.TestCase):

    def setUp(self):
        self.dresser = Dresser()
        self.bed = Bed()
        self.lamp = Lamp()
        self.chair = Chair()
        self.ulamp = UnreachableLamp()
        self.room = Room(name = "Room", objects = [self.dresser, self.bed, self.ulamp], description = '', exits={})
        self.southern_room = Room(name='Southern Room', objects=[self.chair], description='', exits={'north':self.room})
        self.room.exits['south'] = self.southern_room
        self.inv = []

    def tearDown(self):
        pass


    # need to change tests to cope with grammar returning result of getattr instead of grammar returning strings


    # single word action
    def test_direction(self):
        "Direction (either 'n' or 'north') should return ('move', <direction>"
        action = "west"
        self.assertEquals(parse(action, self.room, self.inv), ('move', 'west'))
        action = "n"
        self.assertEquals(parse(action, self.room, self.inv), ('move', 'north'))

    def test_non_direction(self):
        "Verb should return ('verb', None)"
        action = "look"
        self.assertEquals(parse(action, self.room, self.inv), ('look', None))


    # two-word actions
    def test_action_on_item_in_room(self):
        "<action, valid_noun> should return (action, noun)"
        action = "get bed"
        self.assertEquals(parse(action, self.room, self.inv), ('get', 'bed'))

    def test_action_when_two_objects_have_same_name(self):
        "When two objects have the same name, return an error message"
        self.room.objects.append(self.lamp)
        action = "snuff lamp"
        self.assertEquals(parse(action, self.room, self.inv), "More than one object fits that name.")

    def test_action_on_invalid_item(self):
        "Calling an action on an item that does not exist should return an error message"
        action = "get boot"
        self.assertEquals(parse(action, self.room, self.inv), "That object does not exist.")

    def test_name_differentiation_when_one_is_in_container(self):
        """If there are two lamps but one is inside a container, should recognise two lamps 
            when the container is open and only one lamp when when the container is closed"""
        # dresser is closed
        self.dresser.objects.append(self.lamp)
        action = "get lamp"
        self.assertEquals(parse(action, self.room, self.inv), ('get', 'lamp'))
        # dresser is open
        self.dresser.is_open = True
        self.assertEquals(parse(action, self.room, self.inv), "More than one object fits that name.")

    def test_two_word_moving(self):
        "Using a direction in two words (e.g. 'go west') should return ('move', <direction>)"
        action = "go north"
        self.assertEquals(parse(action, self.room, self.inv), ('move', 'north'))

    # three-word actions








if __name__ == "__main__":
    unittest.main()