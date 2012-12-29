from adventure import Room, Object, User

candlestick = Object(name='candlestick')
knife = Object(name='knife')

dining_room = Room(
                name='dining room',
                objects = [candlestick],
                description = "A large room with a long oval table at the center.")

living_room = Room(
                name='living room',
                objects = [knife])

dining_room.exits = {'north': living_room}    
living_room.exits = {'south': dining_room}

bec = User(name='bec', location=dining_room)

