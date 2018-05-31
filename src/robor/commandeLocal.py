"""
fichier de commande du moteur
on le lancera dans un shell
on va faire un thread pour sortir la vitesse
"""

#import serial
import time
import sys
import curses
import queue

from curses import wrapper
from threading import Thread
# initialisation et ouverture du port série
# ser = serial.Serial('/dev/ttyACM0', 19200)


"""
Pour afficher la vitesse en 'temps réel'
"""
class AfficheVitesse(Thread):

    """affichage de la vitesse"""
    def __init__(self, q):
        Thread.__init__(self)
        self._queue = q

    def run(self):
        cmd = ""
        while cmd != "x":
            if (not self._queue.empty()):
                cmd = self._queue.get_nowait()
    #            sys.stdout.write(ser.readline().decode())
                sys.stdout.write('tick')
                print(cmd)
                print("-")
    #            print(ser.readline().decode())
                self._queue.task_done()
            time.sleep(1)

# on passe par un wrapper afin de ne pas perdre le clavier en cas de plantage
def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    aff = AfficheVitesse(q)
    aff.setDaemon(True)
    aff.start()

    # affichage
    stdscr = curses.initscr()
    curses.echo()
    cmd = ""
    while cmd != "x":
        if (cmd != ""):
            cmd = stdscr.getkey()
            q.put(cmd.encode())
#            ser.write(cmd.encode())
    aff.join()
    q.join()



wrapper(main)

#ser.close()

