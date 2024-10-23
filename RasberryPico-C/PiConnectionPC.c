#include "PiConnectionPC.h"
#include "pico/cyw43_arch.h"
#include "config.h"
#include "motor_control.h"

static struct sockaddr_in server_addr, client_addr;
static int sockfd;

void initPiConnection() {
    cyw43_arch_init(); // Initialize the Wi-Fi driver

    // Connect to Wi-Fi
    wlan = network.WLAN(network.STA_IF);
    wlan.active(true);
    wlan.connect(SSID, PASSWORD);

    while (!wlan.isconnected()) {
        printf("Waiting for connection...\n");
        sleep_ms(1000);
    }

    printf("Connected to WiFi\n");
    
    // Set up UDP socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(80);
    
    bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr));
    listen(sockfd, 5); // Listen for incoming connections
}

void parseMessage(const char* message) {
    // Split the message by semicolon
    printf("Received message: %s\n", message);
    char *action_str = strtok(message, ";");
    int action = atoi(action_str);
    int numbers[2];
    int count = 0;

    while (char *num_str = strtok(NULL, ";")) {
        if (count < 2) {
            numbers[count++] = atoi(num_str);
        }
    }

    switch (action) {
        case DRIVE:
            drive(numbers[0], numbers[1]);
            break;
        case STOP_ALL:
            stop_all();
            break;
        default:
            printf("Unknown action: %d\n", action);
            break;
    }
}

void handle_client(int client_fd) {
    char buffer[1024];
    int bytes_received = recv(client_fd, buffer, sizeof(buffer) - 1, 0);
    
    if (bytes_received > 0) {
        buffer[bytes_received] = '\0'; // Null terminate the string
        parseMessage(buffer);
    }
}

