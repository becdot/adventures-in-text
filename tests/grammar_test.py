from grammar import parse, check_noun
from objects import Dresser, Bed, Lamp, Chair, UnreachableLamp
from scaffolding import Room
import unittest

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


    # single word action
    def test_direction(self):
        "Direction should return a Room object if the direction is valid, or an error string if it is not valid"
        action = "south"
        self.assertEquals(parse(action, self.room, self.inv), self.southern_room)
        action = "n"
        self.assertEquals(parse(action, self.room, self.inv), "You cannot go that way.")

    def test_look(self):
        "Verb should return current room's description"
        action = "look"
        self.assertEquals(parse(action, self.room, self.inv), self.room.description)     

    def test_invalid_verb(self):
        "An invalid verb should return an error message"
        action = "jump"
        self.assertEquals(parse(action, self.room, self.inv), "That is not a valid action.")        


    # two-word action
    def test_action_on_item_in_room(self):
        "<action, valid_noun> should perform the appropriate action"
        action = "open dresser"
        self.assertEquals(parse(action, self.room, self.inv), self.dresser.open_description)

    def test_action_when_two_objects_have_same_name(self):
        "When two objects have the same name, return an error message"
        self.room.objects.append(self.lamp)
        action = "snuff lamp"
        self.assertEquals(parse(action, self.room, self.inv), "More than one object fits that name.")

    def test_action_on_invalid_item(self):
        "Calling an action on an item that does not exist should return an error message"
        action = "get boot"
        self.assertEquals(parse(action, self.room, self.inv), "That object does not exist.")

    def test_invalid_action_on_item(self):
        "Calling an invalid action on an existing item should return an error message"
        action = "kick bed"
        self.assertEquals(parse(action, self.room, self.inv), "That is not a valid action.")

    def test_name_differentiation_when_one_is_in_container(self):
        """If there are two lamps but one is inside a container, it should recognise two lamps 
            when the container is open and one lamp when when the container is closed"""
        # dresser is closed
        self.dresser.objects.append(self.lamp)
        action = "get lamp"
        self.assertEquals(parse(action, self.room, self.inv), "That is not a valid action.")
        # dresser is open
        self.dresser.is_open = True
        self.assertEquals(parse(action, self.room, self.inv), "More than one object fits that name.")

    def test_two_word_moving(self):
        "Using a direction in two words (e.g. 'go west') should return a new Room object"
        action = "go south"
        self.assertEquals(parse(action, self.room, self.inv), self.southern_room)

    
    # three-word actions
    def test_action_with_adj_when_two_objects_have_same_name(self):
        """When two objects have the same name but a distinguishing adjective is provided, 
            should perform the action on the correct object"""
        brass_lamp = Lamp()
        brass_lamp.description = "A brass lamp with a tarnished base."
        brass_lamp.on_description = "The light turns on."
        brass_lamp.off_description = "The light turns off."
        self.room.objects.append(brass_lamp)
        # adjective is in object.name
        action = "light brass lamp"
        self.assertEquals(parse(action, self.room, self.inv), brass_lamp.on_description) 
        self.assertTrue(brass_lamp.is_lit)   
        # adjective is in object.description
        action = "snuff tarnished lamp"
        parse(action, self.room, self.inv)
        self.assertFalse(brass_lamp.is_lit)
    
    def test_action_with_unhelpful_adj(self):
        "If adjective is unhelpful but noun does not encounter any conflicts, should call verb on obj"
        self.room.objects.append(self.chair)
        action = "climb sturdy chair"
        self.assertEquals(parse(action, self.room, self.inv), "You clamber onto the object.")

    def test_action_with_unhelpful_adj_and_two_objs_with_same_name(self):
        "If adjective is unhelpful, return error message"
        self.room.objects.append(self.lamp)
        action = "turn_on plaid lamp"
        self.assertEquals(parse(action, self.room, self.inv), "More than one object fits that name.")

    def test_look_in_object(self):
        "'look in' is called as obj.look_in()"
        self.dresser.is_open = True
        action = "look in dresser"
        self.assertEquals(parse(action, self.room, self.inv), "This object is empty.")

    def test_stand_on_object(self):
        "'stand on' is called as obj.stand()"
        self.room.objects.append(self.chair)
        action = "stand on chair"
        self.assertEquals(parse(action, self.room, self.inv), "You clamber onto the object.")        

    def test_invalid_action_with_valid_object(self):
        "An invalid action will return an action-related error message"
        action = "stand on lamp"
        self.assertEquals(parse(action, self.room, self.inv), "That is not a valid action.")                
        action = "spit on bed"
        self.assertEquals(parse(action, self.room, self.inv), "That is not a valid action.")                

    def test_valid_action_with_invalid_object(self):
        "An action performed on an object that doesn't exist will return an error"
        action = "look in chest"
        self.assertEquals(parse(action, self.room, self.inv), "That object does not exist.")


    # four-word actions
    def test_get_down_from_chair(self):
        "Should set has_user to False"
        self.room.objects.append(self.chair)
        self.chair.has_user = True
        action = "get down from chair"
        parse(action, self.room, self.inv)
        self.assertFalse(self.chair.has_user)

    def climb_down_from_chair(self):
        "Should set has_user to False"
        self.room.objects.append(self.chair)
        self.chair.has_user = True
        action = "climb down from chair"
        parse(action, self.room, self.inv)
        self.assertFalse(self.chair.has_user)        

    def stand_on_dark_chair(self):
        "Should set has_User to True"
        self.room.objects.append(self.chair)
        action = "stand on dark chair"
        parse(action, self.room, self.inv)
        self.assertTrue(self.chair.has_user) 

    def turn_on_plaid_lamp(self):
        "Should set is_lit to True"
        action = "turn on plaid lamp"
        self.room.objects.append(self.chair)
        self.chair.has_user = True
        parse(action, self.room, self.inv)
        self.assertTrue(self.ulamp.has_user)

    def get_chair_from_dresser(self):
        "Should add chair to inventory"
        self.dresser.objects.append(self.chair)
        self.dresser.is_open = True
        action = "get chair from dresser"
        parse(action, self.room, self.inv)
        self.assertEquals(self.inv, [self.chair])        









if __name__ == "__main__":
    unittest.main()