int IN1 = 4;    // Input1 conectada al pin 4
int IN2 = 5;    // Input2 conectada al pin 5~
int IN3 = 6;    // Input3 conectada al pin 6~
int IN4 = 8;    // Input4 conectada al pin 8
int ENA = 3;    // ENA conectada al pin 3~
int ENB = 9;    // ENB conectada al pin 9~
int Sensor0 = 0;
int Sensor1 = 0;
int Sensor2 = 0;
int Sensor3 = 0;
void setup()
{
  pinMode (IN1, OUTPUT); 
  pinMode (IN2, OUTPUT); 
  pinMode (IN3, OUTPUT); 
  pinMode (IN4, OUTPUT); 
  pinMode (ENA, OUTPUT);
  pinMode (ENB, OUTPUT);
  pinMode (Sensor0, INPUT);
  pinMode (Sensor1, INPUT);
  pinMode (Sensor2, INPUT);
  pinMode (Sensor3, INPUT);
  Serial.begin(9600); //Inicializo el puerto serial a 9600 baudios
}
  


/*
 Por el momento podemos controlar el arduino de manera remota usando la raspberry pi o bien dejar que siga una linea.
*/
void loop () {
   //Control "Manual" desde raspberry por puerto serial
   if (Serial.available()) { //Si está disponible
      char c = Serial.read(); //Guardamos la lectura en una variable char
      if (c == 'A') { //Enciendo el motor derecho
         digitalWrite(IN3, LOW);
         digitalWrite(IN4, HIGH);
      } else if (c == 'W') { //Enciendo ambos motores
         digitalWrite(IN1, LOW);
         digitalWrite(IN2, HIGH);
         digitalWrite(IN3, LOW);
         digitalWrite(IN4, HIGH);
      } else if (c == 'D') { //Enciendo el motor izquierdo
         digitalWrite(IN1, LOW);
         digitalWrite(IN2, HIGH);
      } else if (c == 'X') { //Enciendo ambos motores (reverse)
         digitalWrite(IN1, HIGH);
         digitalWrite(IN2, LOW);
         digitalWrite(IN3, HIGH);
         digitalWrite(IN4, LOW);
      } else if (c == 'S') { //Apago los motores
         digitalWrite(IN1, LOW);
         digitalWrite(IN2, LOW);
         digitalWrite(IN3, LOW);
         digitalWrite(IN4, LOW);
         analogWrite(ENB,0);
         analogWrite(ENA,0);
      }
     /*else if (c == 'AD') { //Acelera derecha
         analogWrite(ENB,105);
      } else if (c == 'AI') { //Acelera izquierda
         analogWrite(ENA,105);
      }*/
   }
   /*
   //COntrol de seguimiento de linea mediante sensores laser

   if(Sensor4 == HIGH && Sensor3 == HIGH && Sensor2 == LOW && Sensor1 == LOW){

    //Giro izquierda (Rotacion modo tanque)
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);

    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
  }

  else if (Sensor4 == LOW && Sensor3 == LOW && Sensor2 == HIGH && Sensor1 == HIGH){

    //Giro derecha (Rotacion modo tanque)
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
  }

  else{

    //if(Sensor4 == LOW && Sensor3 == HIGH && Sensor2 == HIGH && Sensor1 == LOW

    //Hacia delante
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
  }

   
   */
}
