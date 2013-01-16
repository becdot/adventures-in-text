adventures-in-text
==================

A text-based adventure game framework, written in Python, with aspirations of becoming playable via a Flask site.

Steps:

1. Write the backend in Python
 - Make room, object, and mix-in (e.g. Climbable, Lightable) classes
 - Create a grammar so that the player can type traditional commands (e.g. 'light lamp' vs. 'lamp.light()')
 - Have some sort of global user information (i.e. current location, inventory, etc.) that is passed to necessary objects
2. Use Flask to make a website that can run the game
3. Create some kind of REPL-like interface using javascript that mediates between the player and database
 - Note -- this step is still a bit murky


