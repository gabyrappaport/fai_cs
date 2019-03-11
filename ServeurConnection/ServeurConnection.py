import socket
import sys
from struct import pack

from AI.AlphaBeta import Alphabeta
from AI.Board import Board
from AI.Settings import VAMPIRES, WAREWOLVES


class Client:
    def __init__(self, ai_name, hote="localhost", port=5555):
        self.ai_name = ai_name
        self.hote = "localhost"
        self.port = 5555
        self.connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion_avec_serveur.connect((self.hote, self.port))
        self.board = None
        self.alphabeta = None
        self.open_connexion()

    def open_connexion(self):
        nme = b'NME' + pack("B", len(self.ai_name)) + self.ai_name.encode()
        self.connexion_avec_serveur.send(nme)
        message_recu = self.connexion_avec_serveur.recv(1024)
        while len(message_recu) < 3:
            message_recu += self.connexion_avec_serveur.recv(1024)
        if message_recu[0:3].decode() == "SET":
            message_recu, rows, columns = self.SET(message_recu)
            self.board = Board(rows, columns)
        else:
            raise (Exception("There is a problem in your socket...1"))
        try:
            message_recu, houses_coordinates = self.HUM(message_recu)
            message_recu, our_position = self.HME(message_recu)
            message_recu, initial_coordinates = self.MAP(message_recu)
            self.board.update_board(initial_coordinates)
            if our_position in self.board.vampires.keys():
                self.board.is_playing(VAMPIRES)
                self.alphabeta = Alphabeta(self.board, player=VAMPIRES)
            else:
                self.board.is_playing(WAREWOLVES)
                self.alphabeta = Alphabeta(self.board, player=WAREWOLVES)
            list_moves = self.alphabeta.alphabeta()
            self.move(list_moves)
        except:
            raise (Exception("There is a problem in your socket...2"))
        self.listen()

    def move(self, list_moves):
        nbr_moves = len(list_moves)
        encoded_list_moves = b""
        for m in list_moves:
            encoded_move = pack("B", m[0][0]) + pack("B", m[0][1]) \
                           + pack("B", m[2]) + pack("B", m[1][0]) + pack("B", m[1][1])
            encoded_list_moves += encoded_move  # (pack("d", int(encoded_move)))
        self.connexion_avec_serveur.send(b"MOV" + pack("B", nbr_moves) + encoded_list_moves)

    def listen(self):
        msg_recu = self.connexion_avec_serveur.recv(2048)
        print(msg_recu[0:3].decode())
        if msg_recu[0:3].decode() == "END":
            # on doit coder quelque chose pour réinitialiser et jouer une autre partie
            pass
        elif msg_recu[0:3].decode() == "BYE":
            self.close_connexion()
        elif "UPD" in msg_recu[0:3].decode():
            message_recu, initial_coordinates = self.MAP(msg_recu)
            self.board.update_board(initial_coordinates)
            self.alphabeta.board = self.board
            list_moves = self.alphabeta.alphabeta()
            self.move(list_moves)
            self.listen()

    def SET(self, message):
        while len(message) < 5:
            message += self.connexion_avec_serveur.recv(1024)
        return message[5:], message[3], message[4]

    def HUM(self, message):
        while len(message) < 4:
            message += self.connexion_avec_serveur.recv(1024)
        n_houses = message[3]
        while len(message) < 4 + 2 * n_houses:
            message += self.connexion_avec_serveur.recv(1024)
        houses_coordinates = []
        for i in range(n_houses):
            houses_coordinates.append([message[4 + 2 * i], message[4 + 2 * i + 1]])
        return message[4 + 2 * n_houses:], houses_coordinates

    def HME(self, message):
        while len(message) < 5:
            message += self.connexion_avec_serveur.recv(1024)
        return message[5:], [message[3], message[4]]

    def UPD(self, message):
        print(self.affichage(message[3:]))
        return

    def MAP(self, message):
        while len(message) < 4:
            message += self.connexion_avec_serveur.recv(1024)
        n_map = message[3]
        while len(message) < 4 + 5 * n_map:
            message += self.connexion_avec_serveur.recv(1024)
        initial_coordinates = []  # X, Y, Humans, Vampires, Werewolves
        for i in range(n_map):
            sub_coordinates = []
            for j in range(5):
                sub_coordinates.append(message[4 + 5 * i + j])
            initial_coordinates.append(sub_coordinates)
        return message[4 + 5 * n_map:], initial_coordinates

    def close_connexion(self):
        self.connexion_avec_serveur.close()

    def affichage(self, msg):
        aff = []
        for i in range(0, len(msg)):
            aff.append(msg[i])
        return aff


if __name__ == "__main__":
    ip = sys.argv[2] if len(sys.argv) > 2 else None
    port = sys.argv[3] if len(sys.argv) > 3 else None
    client = Client("We are on fire!", ip, port)
    # ServeurConnection.py –myparams 123.123.3.5 6666
