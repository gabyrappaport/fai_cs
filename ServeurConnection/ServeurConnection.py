import socket
from struct import pack


class Client:
    def __init__(self, ai_name):
        self.ai_name = ai_name
        self.hote = "localhost"
        self.port = 5555
        self.connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion_avec_serveur.connect((self.hote, self.port))
        self.open_connexion()

    def open_connexion(self):
        nme = b'NME' + pack("B", len(self.ai_name)) + self.ai_name.encode()
        self.connexion_avec_serveur.send(nme)
        message_recu = self.connexion_avec_serveur.recv(1024)
        while len(message_recu) < 3:
            message_recu += self.connexion_avec_serveur.recv(1024)
        if message_recu[0:3].decode() == "SET":
            message_recu, rows, columns = self.SET(message_recu)
        else:
            raise (Exception("There is a problem in your socket...1"))
        try:
            message_recu, houses_coordinates = self.HUM(message_recu)
            message_recu, our_position = self.HME(message_recu)
            message_recu, initial_coordinates = self.MAP(message_recu)
        except:
            raise (Exception("There is a problem in your socket...2"))
        self.listen()

    def move(self, nbr_moves, list_moves):
        encoded_list_moves = b""
        for m in list_moves:
            encoded_move = pack("B", m[0]) + pack("B", m[1]) \
                           + pack("B", m[2]) + pack("B", m[3]) + pack("B", m[4])
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
            self.UPD(msg_recu)
            self.move(1, [[4, 3, 4, 4, 4]])
            # compute_next_move(info_De_upd)
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


client = Client("We are on fire")
