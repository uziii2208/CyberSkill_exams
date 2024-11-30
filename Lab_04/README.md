![image](https://github.com/user-attachments/assets/c323ce84-8d14-4ba6-b14a-4c4f1084af34)
# Lab 04 | CyberSkill
## Yêu cầu thực hiện 
```
Lab tuần này:
- 1. Viết một rest api đơn giản bằng golang hỗ trợ 2 path:
   + /date GET trả về thời gian hiện tại của server theo định dạng epoch
   + /infor GET trả về tên của chính bạn
- 2. Viết dockerfile để build app trên thành docker image sử dụng chức năng multi-stage build
- 3. Viết file docker compose để cài container trên và cài thêm nginx container đóng vai trò như webserver cho ứng dụng golang ở trên.
- 4. Build và push docker image lên dockerhub registry
- 5. Dùng github action để triển khai dockcompose trên một máy tính ( sử dụng cloud service hoặc máy tính cá nhân)
```
## Report đề bài
### 1. Viết một REST API đơn giản bằng Golang
- Đầu tiên tôi viết mã Golang và Kiểm tra mã nguồn

![image](https://github.com/user-attachments/assets/6a135f10-5afe-4003-a546-a309521b16cc)

- Kiểm tra REST API (thay vì check bằng Postman thì ta có thể check trên cmd khác SSH qua current server)

![image](https://github.com/user-attachments/assets/dd2748ad-e94c-48f3-8cc6-01ec0f0025df)

- Đảm bảo ứng dụng tự động chạy

![image](https://github.com/user-attachments/assets/63ca173a-0232-4a9c-a069-748529762067)

---

### 2. Viết dockerfile để build app trên thành docker image sử dụng chức năng multi-stage build
- Tiếp theo viết Dockerfile sử dụng multi-stage build

![image](https://github.com/user-attachments/assets/cad680f7-f087-43ff-9767-406dba7f17cb)

- Viết file Docker Compose

![image](https://github.com/user-attachments/assets/4732108e-ded3-485a-983f-aa15e062877c)

- Cấu hình Nginx (nginx.conf) làm reverse proxy cho ứng dụng Golang. File Nginx có thể thêm nhiều mục server nên cứ thoải mái nhé.

![image](https://github.com/user-attachments/assets/db7cbe82-b334-4b95-af0b-9651ddefe8a6)

---

### 3. Build và push docker image lên dockerhub registry
#### Login Docker Hub

- Trước khi tôi đi vào việc Login vào Docker Hub để làm những việc to hơn. Tôi sẽ cài đặt lại toàn bộ Docker

![image](https://github.com/user-attachments/assets/f2744a09-1c4c-4693-b2bf-797c741c2973)

- Cài đặt Docker lại từ đầu

1.	Cập nhật hệ thống:
```
sudo apt update && sudo apt upgrade -y
```

2.	Gỡ cài đặt Docker cũ (nếu chưa làm):
```
sudo apt remove docker docker-engine docker.io containerd runc -y
```

3.	Cài đặt Docker mới nhất:
*	Thêm kho lưu trữ chính thức của Docker:
```
sudo apt install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
*	Cập nhật danh sách package và cài đặt Docker:
```
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
4.	Kiểm tra Docker đã hoạt động chưa:
```
docker --version
docker compose version
```
5.	Thêm quyền cho user hiện tại (để không phải dùng sudo mỗi lần chạy Docker):
```
sudo usermod -aG docker $USER
newgrp docker
```

- Đăng nhập vào Docker Hub

![image](https://github.com/user-attachments/assets/3cae7f4e-9cc2-49ab-a088-a60616599de8)

- Sau đó vào trình duyệt với link trong hình, gõ confirmation code vào thế là xong

![image](https://github.com/user-attachments/assets/2511054d-3b1a-4464-ac92-63746b21b5f5)

![image](https://github.com/user-attachments/assets/d692f8f4-d842-4e2a-b24b-505b41700bae)

---

### 4. Build và push docker image lên dockerhub registry
- Nếu trong quá trình chạy mà bị lỗi như trong hình (‘’can’t copy go.mod & go.sum’’) thì đây là cách giải quyết

![image](https://github.com/user-attachments/assets/bf16754b-d168-4abe-99f2-2ffd98d8644b)

1. Đầu tiên ta phải tạo ```go.mod``` và ```go.sum```

![image](https://github.com/user-attachments/assets/96e83208-24f4-4dbb-b55e-632cebfe0249)

2. Nếu không tạo được file ```go.sum``` thì đây là cách giải quyết

![image](https://github.com/user-attachments/assets/5f0fdc3a-5155-43d8-a80d-1c707c662330)

3. Và sau đó ta tiếp tục Build Docker Image bình thường và check thôi 

![image](https://github.com/user-attachments/assets/395d30c5-258a-4a50-8b18-1c6ad6b482f9)

#### Push Docker Image lên Docker Hub
- Đầu tiên push Image lên Docker Hub

![image](https://github.com/user-attachments/assets/1efd610c-a9fb-42cc-a1bc-66f4ba170b89)

- Check trên Docker Hub

![image](https://github.com/user-attachments/assets/0c25ec59-41d5-4956-b3a5-62f928e80d05)

#### Tóm tắt lệnh quan trọng:
```
# 1. Cài đặt Docker
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER

# 2. Đăng nhập Docker Hub
docker login

# 3. Build image
docker build -t <your-dockerhub-username>/go-app:latest .

# 4. Push image
docker push <your-dockerhub-username>/go-app:latest
```

---

### 5. Dùng github action để triển khai dockcompose trên một máy tính
- Viết workflow cho việc Deploy Docker 

![image](https://github.com/user-attachments/assets/cd926cd7-d881-4fb1-8d7a-650b777e1da9)

- Cấu hình Secrets trong GitHub

![image](https://github.com/user-attachments/assets/b4e104bc-c27a-4740-93a5-fad667298434)

```
Để bảo vệ thông tin nhạy cảm như thông tin đăng nhập Docker Hub và khóa SSH cho máy EC2, bạn cần sử dụng GitHub Secrets:

Truy cập trang GitHub repository của bạn.
Vào Settings > Secrets and variables > Actions > New repository secret.
Thêm các secrets sau:
DOCKER_USERNAME: Tên người dùng Docker Hub của bạn.
DOCKER_PASSWORD: Mật khẩu Docker Hub (hoặc token nếu bạn sử dụng token).
EC2_SSH_KEY: Khóa SSH của bạn (tải từ máy tính EC2, nếu bạn dùng EC2).
EC2_PUBLIC_IP: Địa chỉ IP công cộng của EC2.
```

- Cài đặt Docker Compose trên Máy EC2 (hoặc máy tính cá nhân)
Trên máy EC2 (hoặc máy tính cá nhân mà bạn triển khai Docker Compose), bạn cần cài đặt Docker và Docker Compose nếu chưa cài đặt.

![image](https://github.com/user-attachments/assets/520c8ea8-c661-4115-b501-47aa829bba79)

Cài đặt Docker:
```
sudo apt-get update
sudo apt-get install -y docker.io
```
Cài đặt Docker Compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```



---

## Thông tin 
 - Organization : [Follow link](https://github.com/cyberskill-world)
 - GitHub cá nhân : [Follow link](https://github.com/uziii2208)

---

## Về vấn đề khác...

<div align="center">
<h3 align="center">Nếu có thắc mắc gì về report của mình thì hãy ib lại cho mình nếu có sai sót gì ở đâu đó nhé. Cám ơn rất nhiều !!!!</h3>
<div>

---

 <!-- Support Me --> 
<div align="center">
    <img src="https://github.com/user-attachments/assets/f6a6e4e5-50e6-41d1-81b8-986edaa1a30e" alt="GIF Image">
</div>

