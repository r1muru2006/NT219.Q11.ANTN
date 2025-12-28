# Sử dụng image nền Ubuntu
FROM ubuntu:22.04

# 1. Cài đặt dependencies
RUN apt-get update && apt-get install -y \
    build-essential wget ca-certificates \
    vim gdb strace \
    && rm -rf /var/lib/apt/lists/*

# 2. Tải và biên dịch OpenSSL Vulnerable
# QUAN TRỌNG: Thêm 'no-asm' để tắt toàn bộ tối ưu hóa Assembly (SSE, VPAES, BSAES)
# Điều này ép OpenSSL dùng bảng T-Tables trong code C thuần -> Dính lỗi Cache Timing.
RUN wget https://www.openssl.org/source/openssl-1.1.1w.tar.gz && \
    tar -xzf openssl-1.1.1w.tar.gz && \
    cd openssl-1.1.1w && \
    ./config no-asm --prefix=/usr/local/openssl-vuln && \
    make -j$(nproc) && make install && \
    cd .. && rm -rf openssl-1.1.1w*

# Thiết lập đường dẫn thư viện
ENV LD_LIBRARY_PATH /usr/local/openssl-vuln/lib:$LD_LIBRARY_PATH

# 3. Sao chép mã nguồn PoC
COPY aes_server.c /tmp/
COPY client.c /tmp/

# 4. Biên dịch PoC với thư viện lỗi
# Lưu ý: Server dùng thư viện lỗi (để bị tấn công)
# Client cũng dùng thư viện đó (hoặc system lib đều được, client chỉ cần gửi tin)
RUN gcc /tmp/aes_server.c -o /usr/local/bin/aes_server \
        -I/usr/local/openssl-vuln/include \
        -L/usr/local/openssl-vuln/lib -lcrypto && \
    gcc /tmp/client.c -o /usr/local/bin/client \
        -I/usr/local/openssl-vuln/include \
        -L/usr/local/openssl-vuln/lib -lcrypto -lm && \
    rm /tmp/aes_server.c /tmp/client.c

# WORKDIR để tiện thao tác
WORKDIR /root

CMD ["/bin/bash"]
