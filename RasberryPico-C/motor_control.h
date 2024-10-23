#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

#include "pico/stdlib.h"

// Function prototypes
void setup_motors(void);
void set_motor(const char* motor, int speed);
void stop_all(void);
void move(int speed);
void turn(const char* direction, int speed);
void turn_angle(int angle);
void drive(int angle, int speed);
int getSensorValue(void);
int isBlackDetected(int threshold);

#endif // MOTOR_CONTROL_H
