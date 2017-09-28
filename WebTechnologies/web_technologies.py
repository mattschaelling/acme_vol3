# solutions.py
"""Volume 3: Web Technologies. Solutions File.
Matthew Schaelling
Math 403
September 21, 2017
"""

import json
import socket
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.style.use('fivethirtyeight')


# Problem 1
def prob1(filename="nyc_traffic.json"):
    """Load the data from the specified JSON file. Look at the first few
    entries of the dataset and decide how to gather information about the
    cause(s) of each accident. Make a readable, sorted bar chart showing the
    total number of times that each of the 7 most common reasons for accidents
    are listed in the data set.
    """
    with open(filename, 'r') as f:
        traffic_data = json.load(f)
    reasons = dict()
    for incident in traffic_data:
        for key in incident.keys():
            if 'contributing_factor' in key:
                if key in reasons.keys():
                    reasons[key] += 1
                else:
                    reasons[key] = 0
    '''
        for i in range(1,6):
            factor = 'contributing_factor_vehicle_' + str(i)
            try:
                reason = incident[factor]
            except KeyError as e:
                pass
            else:
                if reason in reasons.keys():
                    reasons[reason] += 1
                else:
                    reasons[reason] = 0
    '''
    reasons = sorted(list(reasons.items()), key = lambda x: x[1], reverse = True)
    graphed_reasons = reasons[:7]
    labels = []
    number = []
    for r in graphed_reasons:
        labels.append(r[0].replace(' ', '\n').replace('/','/\n'))
        number.append(r[1])
    x = np.arange(len(labels))
    plt.figure(figsize = (10,7))
    plt.barh(x, number)
    plt.yticks(x, labels, fontsize = 6)
    plt.show()


class TicTacToe:
    def __init__(self):
        """Initialize an empty board. The O's go first."""
        self.board = [[' ']*3 for _ in range(3)]
        self.turn, self.winner = "O", None

    def move(self, i, j):
        """Mark an O or X in the (i,j)th box and check for a winner."""
        if self.winner is not None:
            raise ValueError("the game is over!")
        elif self.board[i][j] != ' ':
            raise ValueError("space ({},{}) already taken".format(i,j))
        self.board[i][j] = self.turn

        # Determine if the game is over.
        b = self.board
        if any(sum(s == self.turn for s in r)==3 for r in b):
            self.winner = self.turn     # 3 in a row.
        elif any(sum(r[i] == self.turn for r in b)==3 for i in range(3)):
            self.winner = self.turn     # 3 in a column.
        elif b[0][0] == b[1][1] == b[2][2] == self.turn:
            self.winner = self.turn     # 3 in a diagonal.
        elif b[0][2] == b[1][1] == b[2][0] == self.turn:
            self.winner = self.turn     # 3 in a diagonal.
        else:
            self.turn = "O" if self.turn == "X" else "X"

    def empty_spaces(self):
        """Return the list of coordinates for the empty boxes."""
        return [(i,j) for i in range(3) for j in range(3)
                                        if self.board[i][j] == ' ' ]
    def __str__(self):
        return "\n---------\n".join(" | ".join(r) for r in self.board)


# Problem 2
class TicTacToeEncoder(json.JSONEncoder):
    """A custom JSON Encoder for TicTacToe objects."""
    def default(self, obj):
        if not isinstance(obj, TicTacToe):
            raise TypeError("excepted a TicTacToe object for encoding")
        return {'dtype':'TicTacToe Object', 'data':{'board':self.board , 'turn':self.turn, 'winner':self.winner}}


# Problem 2
def tic_tac_toe_decoder(obj):
    """A custom JSON decoder for TicTacToe objects."""
    if "dtype" in obj:
        if item["dtype"] != "TicTacToe Object" or "data" not in obj:
            raise ValueError("Expected a JSON message from TicTacToeEncoder")
        tictactoe = TicTacToe()
        tictactoe.board = obj["data"]['board']
        tictactoe.turn = obj['data']['turn']
        tictactoe.winner = obj['data']['winner']
        return tictactoe
    raise ValueError("Expected a JSON message from TicTacToeEncoder")


def mirror_server(server_address=("0.0.0.0", 33333)):
    """A server for reflecting strings back to clients in reverse order."""
    print("Starting mirror server on {}".format(server_address))

    # Specify the socket type, which determines how clients will connect.
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(server_address)    # Assign this socket to an address.
    server_sock.listen(1)               # Start listening for clients.

    while True:
        # Wait for a client to connect to the server.
        print("\nWaiting for a connection...")
        connection, client_address = server_sock.accept()

        try:
            # Receive data from the client.
            print("Connection accepted from {}.".format(client_address))
            in_data = connection.recv(1024).decode()    # Receive data.
            print("Received '{}' from client".format(in_data))

            # Process the received data and send something back to the client.
            out_data = in_data[::-1]
            print("Sending '{}' back to the client".format(out_data))
            connection.sendall(out_data.encode())       # Send data.

        # Make sure the connection is closed securely.
        finally:
            connection.close()
            print("Closing connection from {}".format(client_address))

def mirror_client(server_address=("0.0.0.0", 33333)):
    """A client program for mirror_server()."""
    print("Attempting to connect to server at {}...".format(server_address))

    # Set up the socket to be the same type as the server.
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(server_address)    # Attempt to connect to the server.
    print("Connected!")

    # Send some data from the client user to the server.
    out_data = input("Type a message to send: ")
    client_sock.sendall(out_data.encode())              # Send data.

    # Wait to receive a response back from the server.
    in_data = client_sock.recv(1024).decode()           # Receive data.
    print("Received '{}' from the server".format(in_data))

    # Close the client socket.
    client_sock.close()


# Problem 3
def tic_tac_toe_server(server_address=("0.0.0.0", 44444)):
    """A server for playing tic-tac-toe with random moves."""
    print("Starting TicTacToe server on {}".format(server_address))

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(server_address)
    server_sock.listen(1)

    # if client wins, send WIN; if full board and no winner, send DRAW; both close connect
    # make move, if server wins send LOSE with object and close connect; 
    # if server doesnt win, send only updated object

    while True:
        print("\nWaiting for a connection...")
        connection, client_address = server_sock.accept()
        def send_back(result, close):
            print("Sending '{}' back to the client.".format(result))
            connection.sendall(out_data.encode())
            if close:
                connection.close()
                print("Closing connection from {}".format(client_address))
        try:
            print("Connection accepted from {}.".format(client_address))
            in_data = connection.recv(1024).decode()
            tictactoe = tic_tac_toe_decoder(in_data)
            spaces = tictactoe.empty_spaces()
            if spaces:
                move = random.choice(spaces)
                try:
                    tictactoe.move(move[0],move[1])
                except ValueError as err:
                    if err == 'the game is over!':
                        if tictactoe.winner == 'O':
                            send_back('WIN', True)
                        else:
                            print('I dont think this was supposed to happen.')
                    if "space" in err and "already taken" in err:
                        print("bad space, closing connection")
                        connection.close()
                        print("Closing connection from {}".format(client_address))
                else:
                    if tictactoe.board == None:
                        out_data = TicTacToeEncoder(tictactoe)
                        connection.sendall(out_data.encode())
                    else:
                        send_back('LOSE', False)
                        out_data = TicTacToeEncoder(tictactoe)
                        connection.sendall(out_data.encode())
                        connection.close()
                        print("Closing connection from {}".format(client_address))
            else:
                out_data = 'DRAW'
                send_back(result, True)


def tic_tac_toe_client(server_address=("0.0.0.0", 44444)):
    """A client program for tic_tac_toe_server()."""
    print("Attempting to connect to server at {}...".format(server_address))
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(server_address)    # Attempt to connect to the server
    tictactoe = TicTacToe()
    while True:
        print(tictactoe.board)
        row = input("Please enter 0,1,2 to select your row: ")
        column = input("Please enter 0,1,2 to select your column: ")
        acceptable = {0,1,2}
        if row not in acceptable or column not in acceptable:
            raise ValueError("Your row or column was not an acceptable input, please try again.")
        else:
            try:
                tictactoe.move(row, column)
            except ValueError as err:
                print(err)
            else:
                out_data = TicTacToeEncoder(tictactoe)
                client_sock.sendall(out_data.encode())
                in_data = client_sock.recv(1024).decode()
                print("Received message from server")
                if in_data == 'WIN':
                    print("Congrats, you're smarter than a really dumb computer")
                    client_sock.close()
                    break
                elif in_data == 'DRAW':
                    print("It's ambigious on whether or not you are smarter than a computer")
                    client_sock.close()
                    break
                elif in_data == 'LOSE':
                    print("You are dumber than a dumb computer")
                    in_board = client_sock.recv(1024).decode()
                    tictactoe = tic_tac_toe_decoder(in_board)
                    print(tictactoe.board)
                    client_sock.close()
                    break
                else:
                    tictactoe = tic_tac_toe_decoder(in_data)
                

# Problem 5
def download_nyc_data():
    """Make requests to download data from the following API endpoints.

    Recycling bin locations: https://data.cityofnewyork.us/api/views/sxx4-xhzg/rows.json?accessType=DOWNLOAD

    Residential addresses: https://data.cityofnewyork.us/api/views/7823-25a9/rows.json?accessType=DOWNLOAD

    Save the recycling bin data as nyc_recycling.json and the residential
    address data as nyc_addresses.json.
    """
    raise NotImplementedError("Problem 5 Incomplete")


# Problem 6
def prob6(recycling="nyc_recycling.json", addresses="nyc_addresses.json"):
    """Load the specifiec data files. Use a k-d tree to determine the distances
    from each address to the nearest recycling bin, and plot a histogram of
    the results.

    DO NOT call download_nyc_data() in this function.
    """
    raise NotImplementedError("Problem 6 Incomplete")
