#include <stdio.h>
#include "pico/stdlib.h"
#include "config.h"
#include "motor_control.h"
#include "PiConnectionPC.h"

void steerMotorsPID(float correction) {
    float base_speed = 0.2;
    float left_speed = base_speed - correction;
    float right_speed = base_speed + correction;

    // Clamp speeds
    left_speed = (left_speed > 1) ? 1 : ((left_speed < -1) ? -1 : left_speed);
    right_speed = (right_speed > 1) ? 1 : ((right_speed < -1) ? -1 : right_speed);

    set_motor("motor1", left_speed * 20); // Scale speed
    set_motor("motor2", right_speed * 20);
}

int main() {
    stdio_init_all();
    setup_motors(); // Initialize motors
    initPiConnection(); // Initialize Wi-Fi connection

    while (1) {
        // Handle incoming client connections and messages
        int client_fd = accept(sockfd, (struct sockaddr *)&client_addr, &client_len);
        if (client_fd >= 0) {
            handle_client(client_fd);
            close(client_fd); // Close the client socket
        }

        // PID Control Logic
        if (isBlackDetected(THRESHOLD)) {
            steerMotorsPID(1.0); // Adjust PID control based on sensor readings
        } else {
            stop_all();
        }
    }

    stop_all(); // Ensure motors are stopped on exit
    return 0;
}
