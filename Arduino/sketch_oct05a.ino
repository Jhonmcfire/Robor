int MoteurA = 2;
int MoteurB = 3;
//definition des differents fonction possible:
void Avancer(int v = 200){
  analogWrite(MoteurA, v);
  analogWrite(MoteurB, v);
}
void Stop() {
  analogWrite(MoteurA, 0);
  analogWrite(MoteurB, 0);
}
void Reculer(int v = 150){
  analogWrite(MoteurA, v);
  analogWrite(MoteurB, v);
}

void setup() {
  // put your setup code here, to run once:
pinMode(MoteurA, OUTPUT);
pinMode(MoteurB, OUTPUT);
Stop();
}

void loop() {
  // put your main code here, to run repeatedly:
  // application des differents fonctions
  Avancer(200);
  delay(2000);
  Stop();
  delay(1000);//pause entree deux instructions:
  Reculer(150);
  delay(1000);
  Stop();
}
