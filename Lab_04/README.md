![image](https://github.com/user-attachments/assets/c323ce84-8d14-4ba6-b14a-4c4f1084af34)
# Lab 03 | CyberSkill
## Yêu cầu thực hiện 
```
Lab tuần này:
- 1. viết một rest api đơn giản bằng golang hỗ trợ 2 path:
   + /date GET trả về thời gian hiện tại của server theo định dạng epoch
   + /infor GET trả về tên của chính bạn
- 2. Viết dockerfile để build app trên thành docker image sử dụng chức năng multi-stage build
- 3. Viết file docker compose để cài container trên và cài thêm nginx container đóng vai trò như webserver cho ứng dụng golang ở trên.
- 4. Build và push docker image lên dockerhub registry
- 5. Dùng github action để triển khai dockcompose trên một máy tính ( sử dụng cloud service hoặc máy tính cá nhân)
```
## Report đề bài
### viết một REST API đơn giản bằng Golang
- Đầu tiên tôi viết mã Golang và Kiểm tra mã nguồn

- Kiểm tra REST API (thay vì check bằng Postman thì ta có thể check trên cmd khác SSH qua current server)

- Đảm bảo ứng dụng tự động chạy

---

### Viết dockerfile để build app trên thành docker image sử dụng chức năng multi-stage build
- Tiếp theo viết Dockerfile sử dụng multi-stage build

- Viết file Docker Compose

- Cấu hình Nginx (nginx.conf) làm reverse proxy cho ứng dụng Golang. File Nginx có thể thêm nhiều mục server nên cứ thoải mái nhé.

---

### Build và push docker image lên dockerhub registry
#### Login Docker Hub

- Trước khi tôi đi vào việc Login vào Docker Hub để làm những việc to hơn. Tôi sẽ cài đặt lại toàn bộ Docker

- Cài đặt Docker lại từ đầu

1.	Cập nhật hệ thống:

‘’
sudo apt update && sudo apt upgrade -y
‘’
2.	Gỡ cài đặt Docker cũ (nếu chưa làm):

‘’
sudo apt remove docker docker-engine docker.io containerd runc -y
‘’
3.	Cài đặt Docker mới nhất:
*	Thêm kho lưu trữ chính thức của Docker:

‘’
sudo apt install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
‘’
*	Cập nhật danh sách package và cài đặt Docker:

‘’
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
‘’
4.	Kiểm tra Docker đã hoạt động chưa:

‘’
docker --version
docker compose version
‘’
5.	Thêm quyền cho user hiện tại (để không phải dùng sudo mỗi lần chạy Docker):

‘’
sudo usermod -aG docker $USER
newgrp docker
‘’

- Đăng nhập vào Docker Hub

- Sau đó vào trình duyệt với link trong hình, gõ confirmation code vào thế là xong

#### Build Docker Image
- Nếu trong quá trình chạy mà bị lỗi như trong hình (‘’can’t copy go.mod & go.sum’’) thì đây là cách giải quyết

1. Đầu tiên ta phải tạo ‘’go.mod’’ và ‘’go.sum’’

2. Nếu không tạo được file ‘’go.sum” thì đây là cách giải quyết

3. Và sau đó ta tiếp tục Build Docker Image bình thường và check thôi 

#### Push Docker Image lên Docker Hub
- Đầu tiên push Image lên Docker Hub

- Check trên Docker Hub


---

#### Tóm tắt lệnh quan trọng:
# 1. Cài đặt Docker
''
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
''
# 2. Đăng nhập Docker Hub
''
docker login
''
# 3. Build image
''
docker build -t <your-dockerhub-username>/go-app:latest .
''
# 4. Push image
''
docker push <your-dockerhub-username>/go-app:latest
''


---

## Thông tin 
 - Organization : [Follow link](https://github.com/cyberskill-world)
 - GitHub cá nhân : [Follow link](https://github.com/uziii2208)

## Về vấn đề khác...

<div align="center">
<h3 align="center">Nếu có thắc mắc gì về report của mình thì hãy ib lại cho mình nếu có sai sót gì ở đâu đó nhé. Cám ơn rất nhiều !!!!</h3>
<div>

<img src="https://github.com/fnky/fnky/raw/fnky/img/smile.gif" alt="Smiley" align="center">
</div>
</div>
<div align="center">
<h3 align="center">Happy Learning / Working !!!</h3>
<div>
<img src="https://github.com/fnky/fnky/raw/fnky/img/smile.gif" alt="Smiley" align="center">
</div>
</div>