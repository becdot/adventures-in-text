adventures-in-text
==================

##An old-school style text-based adventure game framework


###REQUIREMENTS:
------------
- Must have [Python](www.python.org/getit), [Flask](http://flask.pocoo.org/) and [pymongo](https://pypi.python.org/pypi/pymongo/) installed.

###OVERVIEW:
------------
- A sample game can be previewed [here](http://ec2-54-244-180-72.us-west-2.compute.amazonaws.com/adventure)
- After installing, the sample game can also be run with the shell command `python game_site.py` and accessed at http://localhost:5000
- Users can enter actions and interact with objects!
- Games are saved using a custom serialisation method, and stored in a MongoDB database
- Uses Flask sessions to remember which game is associated with a particular browser, so that users can go back to their last game

###GAME CREATION:
------------
####You can easily create your own game world and play it using the built-in game engine
- Rooms
   * Defined in scaffolding.py
   * Syntax -> Room(name, list_of_objects, description, dictionary_of_exits)
- Objects
   * Inherit from Object (scaffolding.py) and any number of Mix-ins (properties.py)
   * Defined by a dictionary that must contain a list of bases, a dictionary of attributes, and a dictionary of methods (objects.py)
   * Created dynamically in creation.py, using the object's information dictionary

```
   chair_dict = {'bases': (Climbable, Gettable, Object),
                  'attributes': {'id': "chair", 'name': "chair", 'has_user': False, 
                  'description': "A sturdy wooden chair with dark wooden slats."}}
```
- Game
   * A class that must create all objects and rooms in the init method
   * Once all rooms and objects are created, should be stored in the form:
   `game = {'rooms': [room1, room2], 'location': room1, 'inv': [key]}`
   * Example game can be found in test_game.py
- Game engine
   * All game functionality is defined in game.py
   * To add a different game, replace `from test_game import TestGame` with `from your_game_file import MyGameClass` and replace `base = TestGame()` with `base = MyGameClass()`
   * Run the game in the shell with the command `python game_site.py` and visit http://localhost:5000 to play!
- Additionals
   * Running the game with Flask happens in game_site.py
   * User action parsing is taken care of by grammar.py
   * HTML can be found in the static folder
- Bugs
   * An incomplete list of these can be found in To do!
