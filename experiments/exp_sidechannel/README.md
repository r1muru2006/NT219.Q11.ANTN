# Build image
docker build -t aes-timing-attack .

# Run container và ghim vào Core 0 (hoặc core bất kỳ)
# --cpuset-cpus="0": Bắt buộc cả container chỉ chạy trên 1 core vật lý
docker run -it --rm --cpuset-cpus="0" aes-timing-attack
