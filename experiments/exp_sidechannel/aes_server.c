// aes_server.c - Real AES Timing Vulnerable Server
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <openssl/aes.h>
#include <time.h>

// Hàm in khóa để debug
void print_hex(const char *label, const unsigned char *data, size_t len) {
    printf("%s: ", label);
    for (size_t i = 0; i < len; i++) printf("%02X", data[i]);
    printf("\n");
}

int main() {
    int sockfd;
    struct sockaddr_in servaddr, cliaddr;
    socklen_t addr_len;
    unsigned char plaintext[16];
    unsigned char ciphertext[16];
    AES_KEY aes_key;
    
    // Khóa cố định (hoặc random) để ta có thể kiểm chứng tấn công
    unsigned char key[16] = "secret_data_leak";

    // Tắt buffering của stdout để log hiện ngay lập tức
    setvbuf(stdout, NULL, _IONBF, 0);

    print_hex("Server Key", key, 16);

    // Vì chúng ta dùng OpenSSL build với "no-asm", 
    // AES_set_encrypt_key sẽ chuẩn bị các T-Tables trong RAM.
    AES_set_encrypt_key(key, 128, &aes_key);

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(12345);

    if (bind(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr)) < 0) {
        perror("bind");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("AES server (Vulnerable Version) listening on 0.0.0.0:12345...\n");

    // Tăng độ ưu tiên tiến trình (nếu có quyền root trong docker)
    // nice(-20); 

    while (1) {
        addr_len = sizeof(cliaddr);
        ssize_t n = recvfrom(sockfd, plaintext, sizeof(plaintext), 0,
                             (struct sockaddr*)&cliaddr, &addr_len);
        
        if (n != 16) continue; // Chỉ xử lý gói 16 byte

        // ĐIỂM MẤU CHỐT:
        // Hàm này sẽ truy cập T-Tables (Te0, Te1, Te2, Te3).
        // Nếu Te[plaintext ^ key] không nằm trong Cache L1 -> Mất nhiều cycle hơn.
        AES_encrypt(plaintext, ciphertext, &aes_key);

        sendto(sockfd, ciphertext, sizeof(ciphertext), 0,
               (struct sockaddr*)&cliaddr, addr_len);
    }
    close(sockfd);
    return 0;
}
