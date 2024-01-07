#  Computer Project #7
#
# Algorithm
#  program that allows the user to play Nine Men’s Morris according to the
#  rules outlined above the game continues until a players piece is less than 3 or
#  when the quit command is not entered. when a mill is formed, a piece is removed from the game and will never be
#  played again. In phase 1, the game runs and each player alternates to place their 9 pieces
#  after phase 2 begin, where each player moves their pieces placed until a winner is formed or q command entered.
########################################################### '''


import sys
import NMM  # This is necessary for the project

BANNER = """
    __      _(_)_ __  _ __   ___ _ __| | |
    \ \ /\ / / | '_ \| '_ \ / _ \ '__| | |
     \ V  V /| | | | | | | |  __/ |  |_|_|
      \_/\_/ |_|_| |_|_| |_|\___|_|  (_|_)
"""

RULES = """                                                                                       
    The game is played on a grid where each intersection is a "point" and
    three points in a row is called a "mill". Each player has 9 pieces and
    in Phase 1 the players take turns placing their pieces on the board to 
    make mills. When a mill (or mills) is made one opponent's piece can be 
    removed from play. In Phase 2 play continues by moving pieces to 
    adjacent points. 
    The game is ends when a player (the loser) has less than three 
    pieces on the board.
"""

MENU = """
    Game commands (first character is a letter, second is a digit):
    xx        Place piece at point xx (only valid during Phase 1 of game)
    xx yy     Move piece from point xx to point yy (only valid during Phase 2)
    R         Restart the game
    H         Display this menu of commands
    Q         Quit the game

"""


## Uncomment the following lines when you are ready to do input/output tests!
## Make sure to uncomment when submitting to Codio.
def input(prompt=None):
    if prompt != None:
        print(prompt, end="")
    aaa_str = sys.stdin.readline()
    aaa_str = aaa_str.rstrip("\n")
    print(aaa_str)
    return aaa_str


def validate_mill(board, player, destination):
    '''
        checks the destination/player's move to check if mill is formed
    '''
    positions = board.points
    for mill in board.MILLS:
        if (destination in mill
                and player == positions[mill[0]] and player == positions[mill[1]] and player == positions[mill[2]]):
            return True
    return False


def count_mills(board, player):
    """
        return count the number of mills formed for player
    """
    count = 0
    positions = board.points
    for mill in board.MILLS:
        if positions[mill[0]] == player and positions[mill[1]] == player and positions[mill[2]] == player:
            count += 1
    return count


def place_piece_and_remove_opponents(board, player, destination):
    """
        check if the destination of player is empty then
          and if a mill if formed, remove a pice not mill from the opponents plays
        if not empty raise an error
    """
    positions = board.points
    if positions[destination].isspace():
        board.assign_piece(player, destination)
        if validate_mill(board, player, destination):
            print('A mill was formed!')
            remove_piece(board, player)
    else:
        raise RuntimeError("Invalid command: Destination point already taken")


def move_piece(board, player, origin, destination):
    """
       loop and check and raise errors when game receives invalid inputs
       until correct command is entered then break else continue

       Raises:
        - RuntimeError: If the command is invalid or the specified point is not eligible for removal.

       Moves the player's piece from one location to the next
    """
    plays = board.ADJACENCY
    while True:
        try:
            positions = board.points
            if len(origin) != 2 or len(destination) != 2:
                raise RuntimeError("Invalid number of points")
            if destination not in board.points:
                raise RuntimeError('Invalid command: Not a valid point')
            if destination.isspace() is False and destination not in plays[origin] and destination not in positions:
                raise RuntimeError("Invalid command: Not a valid point")
            if destination not in plays[origin] and destination in positions:
                raise RuntimeError("Invalid command: Destination is not adjacent")
            if positions[origin] == get_other_player(player):
                raise RuntimeError("Invalid command: Origin point does not belong to player")
            else:
                board.clear_place(origin)
                board.assign_piece(player, destination)
                break
        except RuntimeError as error:
            print("{:s}\nTry again.".format(str(error)))
        print(board)
        print(player + "'s turn!")
        command = input("Move a piece (source,destination) :> ").strip().lower().split()
        origin = command[0]
        destination = command[1]
        continue


def points_not_in_mills(board, player):
    """
        loop through the board class of mills
          check if each mill is in plays and subtract from the cpy
        return cpy(remaining point not in mill)

    """
    plays = placed(board, player)
    sub = set(plays)
    cpy = sub.copy()
    for mill in board.MILLS:
        if set(mill) < sub:
            cpy -= set(mill)
    return cpy


def placed(board, player):
    """
        check each position in the board of a player and store it up in a a list
        return the list of plays
    """
    positions = list()
    player_positions = board.points
    for i in player_positions:
        if player_positions[i] == player:
            positions.append(i)
    return positions


def remove_piece(board, player):
    """
        Allows a player to remove an opponent's piece from the board after forming a mill.

        Parameters:
        - board (NMM.Board): The game board.
        - player (str): The current player ("X" or "O").

        Raises:
        - RuntimeError: If the command is invalid or the specified point is not eligible for removal.

        Returns:
        - None: Modifies the game board in place.
    """
    positions = board.points
    print()
    print(board)
    opponent = get_other_player(player)
    not_mill_pt = list(points_not_in_mills(board, opponent))
    played = set(placed(board, opponent))
    not_mill_set = set(not_mill_pt)
    mill_pt = played - not_mill_set
    # r = [item for item in not_mill_pt if item not in played]
    while True:
        try:
            piece = input('Remove a piece at :> ').strip().lower()
            if len(piece) != 2:
                raise RuntimeError("Invalid command: Not a valid point")

            if positions[piece] == opponent and piece not in not_mill_pt and len(not_mill_pt) > 0:
                raise RuntimeError('Invalid command: Point is in a mill')
            if positions[piece] == player or positions[piece].isspace():
                raise RuntimeError("Invalid command: Point does not belong to player")
            else:
                if len(not_mill_pt) > 0:
                    not_mill_pt.remove(piece)
                    board.clear_place(piece)
                else:
                    mill_pt.remove(piece)
                    board.clear_place(piece)
                break

        except RuntimeError as error:
            print("{:s}\nTry again.".format(str(error)))


def is_winner(board, player):
    """
        return True if the opponent plays is less than 3
    """
    opponent = get_other_player(player)
    opponent_plays = placed(board, opponent)
    if len(opponent_plays) < 3:
        return True
    else:
        return False


def get_other_player(player):
    """
       get the opponent signature and return it
    """
    return "X" if player == "O" else "O"


def main():
    # Loop so that we can start over on reset
    while True:
        # Setup stuff.
        print(RULES)
        print(MENU)
        board = NMM.Board()
        print(board)
        player = "X"
        print(player + "'s turn!")
        placed_count = 0  # total of pieces placed by "X" or "O", includes pieces placed and then removed by opponent

        # PHASE 1

        # placed = 0
        command = input("Place a piece at :> ").strip().lower()
        print()
        # Until someone quits or we place all 18 pieces...
        while command != 'q' and placed_count != 18:
            placed_count += 1
            try:
                place_piece_and_remove_opponents(board, player, command)
                # checks and remove player if mill is formed
                if validate_mill(board, player, command[1]):
                    print('A mill was formed!')
                    remove_piece(board, player)
            # Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
                continue

            # Prompt again
            print(board)
            player = get_other_player(player)
            print(player + "'s turn!")
            if placed_count < 18:
                # print(player + "'s turn!")
                command = input("Place a piece at :> ").strip().lower()
                # Print Menu
                if command == 'h':
                    print(MENU)
                    command = input("Place a piece at :> ").strip().lower()
                if command == 'r':
                    break
                # If we ever quit we need to return
                if command == 'q':
                    return
            else:
                print("**** Begin Phase 2: Move pieces by specifying two points")
                command = input("Move a piece (source,destination) :> ").strip().lower()
                break
            print()
        # start over again
        if command == 'r':
            continue
        # If we ever quit we need to return
        if command == 'q':
            return

        # PHASE 2 of game
        while command != 'q':
            # commands should have two points
            try:
                command = command.split()
                move_piece(board, player, command[0], command[1])
                # checks and remove player if mill is formed
                if validate_mill(board, player, command[1]):
                    print('A mill was formed!')
                    remove_piece(board, player)
                if is_winner(board, player):
                    print(BANNER)
                    break

                # display_board(board)
                print(board)
                player = get_other_player(player)
                print(player + "'s turn!")
                command = input("Move a piece (source,destination) :> ").strip().lower()

                # check if cammand is valid for the form xx yy
                while len(command.split()) != 2:
                    print("Invalid number of points\nTry again.")
                    print(board)
                    print(player + "'s turn!")
                    command = input("Move a piece (source,destination) :> ").strip().lower()

                # check winner
                if is_winner(board, player) is True:
                    print(BANNER)
                    break
                else:
                    if command == 'h':
                        print(MENU)
                        command = input("Place a piece at :> ").strip().lower()
                    if command == 'r':
                        break
                    # If we ever quit we need to return
                    if command == 'q':
                        return
                    continue

            # Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
                # Display and re_prompt

        break


if __name__ == "__main__":
    main()
