"""
    gestion des moteurs en python
    on va essayer de faire le miroir d'arduino avec la bibliothèque GPIO
    réf https://deusyss.developpez.com/tutoriels/RaspberryPi/PythonEtLeGpio/
    explication du pwm http://www.locoduino.org/spip.php?article47

    prérequis : installation de la librairie GPIO (avoir pip installé)
    pip install RPi.GPIO
"""

# on import GPIO
#import RPi.GPIO as GPIO

"""
    on ne connait pas la numérotation employée, mais on peut la choisir
    GPIO.setmode(GPIO.BOARD) les n° comme sur la carte
    GPIO.setmode(GPIO.BCM) numérotation de la puce
    on peut récupérer le mode employé par GPIO.getmode()
"""

# pin arduino des moteurs
PIN_MOTEUR_DROIT = 6
PIN_MOTEUR_GAUCHE = 5
PIN_CTRL_DROIT = 7
PIN_CTRL_GAUCHE = 4
PIN_DETECTEUR = 2

# distance parcourue entre 2 ticks
FRAC_DISTANCE = 0.05

# temps entre 2

"""
On va définir une classe Moteur avec les attributs :
- pin : où est connecté le moteur
- vitesse : ce sera 0 ou 255
- sens : en avant ou en arriere (AVANCE, RECULE)
"""
class Moteur:
    """Objet représentant un moteur"""

# dans le constructeur on met le pin ou est connecté le moteur
# par défaut on avance
    def __init__(self, pin):
        self._pin = pin
        self._sens = 'AVANCER'

# démarrer le moteur
    def demarrer(self):
        self._vitesse = 255

# arreter le moteur
    def arreter(self):
        self._vitesse = 0

# fixer la vitesse
    def accelerer(self, vitesse):
        self._vitesse = vitesse

# pour avancer
    def marcheAvant(self):
        self._sens = 'AVANCE'

# pour reculer
    def marcheArriere(self):
        self._sens = 'RECULE'

"""
On va définir une classe pour le détecteur
"""
class Detecteur:
    """
    Sur le détecteur sera placé un callback sur le front montant
    http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-2
    """
    def __init__(self, pin):
        self._pin = pin
#        GPIO.add_event_detect(self._pin, GPIO.RISING, callback=self.ajoutDistance, bouncetime=10)

    """
    à chaque tick, on ajoute la distance parcourue    
    """
    def ajoutDistance(self):
        self._distance = self._distance + FRAC_DISTANCE


"""
Définition de notre desserte
"""
class Desserte:
    """
    Elle est composée de 2 moteurs : un droit et un gauche
    """
    def __init__(self, moteurDroit, moteurGauche, detecteur):
        self._moteurDroit = moteurDroit
        self._moteurGauche = moteurGauche
        self._detecteur = detecteur

    """
    Pour avancer, on met les 2 moteurs en marche avant
    """
    def marcheAvant(self):
        self._moteurDroit.marcheAvant()
        self._moteurGauche.marcheAvant()

    """
    Pour reculer, on met les 2 moteurs en marche arrière
    """
    def marcheAvant(self):
        self._moteurDroit.marcheArriere()
        self._moteurGauche.marcheArriere()

    """
    Pour démarrer, on démarre les 2 moteurs
    """
    def demarrer(self):
        self._moteurDroit.demarrer()
        self._moteurGauche.demarrer()

    """
    Pour s'arrêter, on arrête les 2 moteurs
    """
    def arreter(self):
        self._moteurDroit.arreter()
        self._moteurGauche.arreter()

    """
    Pour tourner à droite, on arrête le moteur droit
    """
    def tournerADroite(self):
        self._moteurDroit.marcheArriere()
        self._moteurGauche.marcheAvant()

    """
    Pour tourner à gauche, on arrête le moteur gauche
    """
    def tournerAGauche(self):
        self._moteurDroit.marcheAvant()
        self._moteurGauche.marcheArriere()

    """
    Pour aller tout droit, on démarre les 2 moteurs
    """
    def allerToutDroit(self):
        self._moteurDroit.demarrer()
        self._moteurGauche.demarrer()

# test des moteurs
motor1 = Moteur(1)
#motor1.avance()
motor1.demarrer()
#print(motor1)
#print(motor1._pin)
print(motor1.__dict__)
motor1.marcheArriere()
print(motor1.__dict__)

# création de la desserte
d = Desserte(Moteur(PIN_MOTEUR_DROIT), Moteur(PIN_MOTEUR_GAUCHE), Detecteur(PIN_DETECTEUR))
print(d.__dict__)
print(d._moteurDroit.__dict__)
print(d._moteurGauche.__dict__)
