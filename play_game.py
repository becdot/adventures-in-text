# import scaffolding # sets base verbs on Object class
# from grammar import parse

# def play_game(game, action):
#     """Takes a game dictionary and an action and attempts to call the action.  
#     Returns a tuple of the updated game dictionary and any messages."""
#     location = game['location']
#     inventory = game['inv']
#     message = None

#     moved = parse(action, location, inventory)
#     if isinstance(moved, scaffolding.Room):
#         game['location'] = moved
#         return (game, None)
#     return (game, moved)

