#include "motor_control.h"
#include "pico/stdlib.h"
#include <string.h>
#include <stdio.h>

const int motor_pins[4] = {13, 12, 11, 10}; // motor1_forward, motor1_backward, motor2_forward, motor2_backward
uint pwm_slice_num_t pwm1, pwm2;

void setup_motors() {
    for (int i = 0; i < 4; i++) {
        gpio_init(motor_pins[i]);
        gpio_set_dir(motor_pins[i], GPIO_OUT);
    }

    pwm1 = pwm_gpio_to_slice_num(motor_pins[0]);
    pwm2 = pwm_gpio_to_slice_num(motor_pins[2]);

    pwm_set_clkdiv(pwm1, 125.0f); // Set clock divider
    pwm_set_clkdiv(pwm2, 125.0f); // Set clock divider
    pwm_set_wrap(pwm1, 65535);
    pwm_set_wrap(pwm2, 65535);
}

void set_motor(const char* motor, int speed) {
    int forward_pin = (strcmp(motor, "motor1") == 0) ? motor_pins[0] : motor_pins[2];
    int backward_pin = (strcmp(motor, "motor1") == 0) ? motor_pins[1] : motor_pins[3];

    // Clamp speed between -100 and 100
    if (speed > 100) speed = 100;
    if (speed < -100) speed = -100;

    if (speed > 0) {
        gpio_put(forward_pin, 1);
        gpio_put(backward_pin, 0);
    } else if (speed < 0) {
        gpio_put(forward_pin, 0);
        gpio_put(backward_pin, 1);
    } else {
        gpio_put(forward_pin, 0);
        gpio_put(backward_pin, 0);
        return;
    }

    int duty_cycle = (speed > 0) ? (speed * 65535 / 100) : 0;
    pwm_set_chan_level(pwm1, PWM_CHAN_A, duty_cycle); // Set PWM for motor1
    pwm_set_chan_level(pwm2, PWM_CHAN_A, duty_cycle); // Set PWM for motor2
}

void stop_all() {
    for (int i = 0; i < 4; i++) {
        gpio_put(motor_pins[i], 0);
    }
    pwm_set_chan_level(pwm1, PWM_CHAN_A, 0);
    pwm_set_chan_level(pwm2, PWM_CHAN_A, 0);
}

// Dummy sensor value function for testing
int getSensorValue(void) {
    // Replace with actual sensor reading code
    return rand() % 10000; // Simulated sensor value
}

int isBlackDetected(int threshold) {
    int sensor_value = getSensorValue();
    return sensor_value < threshold; // Change this condition as needed
}

// Other functions such as move, turn, turn_angle, and drive can be implemented similarly.
void turn(const char* direction, int speed) {
    if (strcmp(direction, "left") == 0) {
        set_motor("motor1", -speed);
        set_motor("motor2", speed);
    } else if (strcmp(direction, "right") == 0) {
        set_motor("motor1", speed);
        set_motor("motor2", -speed);
    }
}

void turn_angle(int angle) {
    int time_to_turn = abs(angle) / DEGREES_PER_SECOND * 1000; // Convert to milliseconds
    if (angle > 0) {
        turn("left", TURN_SPEED);
    } else {
        turn("right", TURN_SPEED);
    }
    sleep_ms(time_to_turn); // Wait the required time
    stop_all(); // Stop the motors after turning
}

void drive(int angle, int speed) {
    speed *= 0.1;
    if (angle < 0) {
        set_motor("motor1", speed);
        set_motor("motor2", speed * (1 + angle / 128));
    } else {
        set_motor("motor1", speed * (1 - angle / 128));
        set_motor("motor2", speed);
    }
}
