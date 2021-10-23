from enum import Enum

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

class Room:
    def __init__(self, room_dict, pos, dest):
        self.__room_dict = room_dict
        self.__pos = pos
        self.__dest = dest

    def __move(self, messages, pos):
        x, y = pos
        if not (x, y) in self.__room_dict:
            messages.append("You cannot go there")
            return False
        else:
            self.__pos = (x, y)
            room_name = self.__room_dict[self.__pos]
            messages.append(f"You are in the {room_name}")
        if self.__room_dict[self.__pos] == self.__dest:
            messages.append("You rechead your destination!")
        return True


    def move(self, direction, steps):
        messages = []
        for i in range(steps):
            x, y = self.__pos
            if direction == Direction.NORTH:
                y += 1
            elif direction == Direction.SOUTH:
                y -= 1
            elif direction == Direction.WEST:
                x -= 1
            elif direction == Direction.EAST:
                x += 1
            if not self.__move(messages, (x, y)):
                return messages
        return messages    


if __name__ == '__main__':
    room_dict = {(1,1): 'Dungeon', (2,1): 'Corridor', (3,1): 'Armory', (1,2) : 'Bedroom', (2,2) : 'Hall', (3,2) : 'Kitchen', (2,3) : 'Balcony'}
    start_pos = (1,1)
    room = Room(room_dict, start_pos)
    messages = room.move(Direction.NORTH, 1)
    print(messages)
