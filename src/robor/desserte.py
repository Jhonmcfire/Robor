"""
    Commmande de la desserte

    On utilisera les bibliothèques
    - curses pour afficher la vitesse et l'état du robot
    - time pour faire de la temporisation
    - serial pour communiquer avec l'Arduino
    - Thread afin de pouvoir communiquer avec l'Arduino en même temps que d'afficher la vitesse

    On fera un object Desserte pour commander l'Arduino qui gèrera les moteurs.
    Il vaut mieux laisser la gestion bas niveau à l'Arduino et laisser le Raspberry gérer
    la caméra et le site web
    On séparera la communication le l'affichage en faisant de petites méthodes utilitaires

"""

import serial
import time
import curses

from curses import wrapper
from threading import Thread

# on place les paramètres de communication en constante
PORT = '/dev/ttyACM0'
VITESSE_PORT = 19200

"""
La desserte est un thread que l'on peut commander
Elle va afficher tte les 1/2 s la vitesse
Même si les commandes de la desserte sont les mêmes que celles du robot,
par sécurité, on passera par une fonction de commande
"""
class Desserte(Thread):
    """Commande de la desserte"""

    # en paramètre, on passe l'écran
    def __init__(self, stdscr):
        Thread.__init__(self)     # initialisation du thread
        self._stdscr = stdscr
        self._cmd = ""
        self.init()

    # affichage et attente de la commande
    def run(self):
        # affichage
        self._stdscr.addstr(0, 1, '=' * 20)
        self._stdscr.addstr(1, 1, 'ROBOR')
        self._stdscr.addstr(2, 1, '=' * 20)
        self._stdscr.addstr(3, 1, 'Vitesse  :', curses.A_BOLD)
        self._stdscr.addstr(4, 1, 'Etat     :', curses.A_BOLD)
        self._stdscr.addstr(4, 12, "ARRETE         ", curses.A_REVERSE)
        self._stdscr.addstr(6, 1, "Commandes :", curses.A_BOLD)
        self._stdscr.addstr(7, 4, "z -> Avancer")
        self._stdscr.addstr(8, 4, "q -> Tourner à gauche")
        self._stdscr.addstr(9, 4, "s -> Reculer")
        self._stdscr.addstr(10, 4, "d -> Tourner à droite")
        self._stdscr.addstr(11, 4, "x -> Arrêter")
        self._stdscr.addstr(12, 4, "w -> Sortir")
        while(self._cmd != "w"):
            self._stdscr.addstr(3, 12, "{0} cm/s".format(self.litVitesse()))
            if (self._cmd == 'z'):
                self.envoieCommande("z")
                self._stdscr.addstr(4, 12, "AVANCE         ", curses.A_REVERSE)
            elif (self._cmd == 'q'):
                self.envoieCommande("q")
                self._stdscr.addstr(4, 12, "TOURNE A GAUCHE", curses.A_REVERSE)
            elif (self._cmd == 's'):
                self.envoieCommande("s")
                self._stdscr.addstr(4, 12, "RECULE         ", curses.A_REVERSE)
            elif (self._cmd == 'd'):
                self.envoieCommande("d")
                self._stdscr.addstr(4, 12, "TOURNE A DROITE", curses.A_REVERSE)
            elif (self._cmd == 'x'):
                self.envoieCommande("x")
                self._stdscr.addstr(4, 12, "ARRETE         ", curses.A_REVERSE)

            self._stdscr.refresh()
            # on attend 1/2s afin de laisser les autres processus tourner
            time.sleep(0.5)
        self.sortie()

    # pour éviter les locks
    def cmd(self, cmd):
        self._cmd = cmd

    """
    gestion du port série
    """
    # ouverture à l'initialisation
    def init(self):
        self._serial = serial.Serial(PORT, VITESSE_PORT)

    # fermeture en sortie
    def sortie(self):
        self._serial.close()

    # lecture de vitesse
    def litVitesse(self):
        return self._serial.readline().decode()[:-2]

    # envoi de la commande
    def envoieCommande(self, commande):
        self._serial.write(commande)

# lancement principal
def main(stdscr):
    # affichage
    # initialisation de curses
    stdscr = curses.initscr()
    # pour bouger le curseur le moins possible
    stdscr.leaveok(True)
    stdscr.clear()
    stdscr.refresh()

    # création de la desserte avec l'écran en paramètre
    # afin qu'elle puisse gérer l'affichage
    d = Desserte(stdscr)
    # on la place en démon pour la laisser tourner en tâche de fond
    d.daemon = True
    # démarrage de la desserte (exécution de la fonction run())
    d.start()
    # on attend que la desserte ait démarrée
    time.sleep(1)
    # initialisation de la commande (on quitte sur un w)
    cmd = ""
    while (cmd != "w"):
        # peut importe la casse de la commande
        cmd = stdscr.getkey().lower()
        # on passe la commande à la desserte
        d.cmd(cmd)
    # la desserte ayant reçu la commande de sortie, on attend qu'elle se ferme correctement
    d.join()


# utilisation du wrapper de curses afin de récupérer le terminal (voir doc)
wrapper(main)
