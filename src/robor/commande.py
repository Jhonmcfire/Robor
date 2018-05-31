"""
fichier de commande du moteur
on le lancera dans un shell
on va faire un thread pour sortir la vitesse
"""

import serial
import time
import sys
import curses
import Queue

from curses import wrapper
from threading import Thread
# initialisation et ouverture du port série
ser = serial.Serial('/dev/ttyACM0', 19200)

queue = Queue.Queue()

"""
Pour afficher la vitesse en 'temps réel'
"""
class AfficheVitesse(Thread):

    """affichage de la vitesse"""
    def __init__(self, queue):
        Thread.__init__(self)
        self._queue = queue

    def run(self):
        cmd = ""
        while cmd != "x":
            cmd = self._queue.get_nowait()
            sys.stdout.write(ser.readline().decode())
            print(cmd)
            print("-")
            print(ser.readline().decode())
            time.sleep(1)



aff = AfficheVitesse()
aff.start()

# affichage
stdscr = curses.initscr()
curses.echo()

# on passe par un wrapper afin de ne pas perdre le clavier en cas de plantage
def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    cmd = ""
    while cmd != "x":
        if (cmd != ""):
            cmd = stdscr.getkey()
            queue.put(cmd.encode())
            ser.write(cmd.encode())



wrapper(main)

aff.join()
ser.close()

