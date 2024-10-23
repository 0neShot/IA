#ifndef CONFIG_H
#define CONFIG_H

#define DRIVE 1
#define STOP_ALL 2

// Definitions for Robot
#define THRESHOLD 5000
#define ANALOG_SENSOR_PIN 28
#define ONBOARD_LED_PIN 25

// Motor Definitions
#define PWM_FREQUENCY 40
#define TURN_SPEED 20  // % of maximum turn speed
#define DEGREES_PER_SECOND 90 // degrees per second

// Constants for PID
#define KP 1.0
#define KI 0.1
#define KD 0.05

// WiFi Connection Settings
#define SSID "DESKTOP-12QN0M"
#define PASSWORD "6d]9129K" // Consider securing this

#endif // CONFIG_H
