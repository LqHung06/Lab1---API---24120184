# 👨‍🎓 Thông tin sinh viên
* **MSSV:** 24120184
* **Họ Tên:** Lê Quốc Hưng
* **Lớp:** 24CTT3

# 🖼️ Image Captioning API

## 1. Tên mô hình và liên kết tới Hugging Face
* **Tên mô hình:** BLIP (Bootstrapping Language-Image Pre-training) - Phiên bản `Salesforce/blip-image-captioning-base`
* **Liên kết Hugging Face:** [Salesforce/blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base)

## 2. Mô tả ngắn về chức năng của hệ thống
* Hệ thống là một Web API được xây dựng bằng FastAPI, tích hợp trí tuệ nhân tạo để xử lý thị giác máy tính và ngôn ngữ tự nhiên. Chức năng chính của hệ thống là nhận đầu vào là một tệp hình ảnh từ người dùng và tự động sinh ra một câu văn bản mô tả ngữ cảnh, nội dung của bức ảnh đó bằng tiếng Anh.

## 3. Hướng dẫn cài đặt thư viện
Yêu cầu hệ thống đã cài đặt sẵn Python. Tùy thuộc vào môi trường làm việc, bạn thực hiện cài đặt theo một trong hai cách sau:
### Trên máy cá nhân (Local)
* Khuyến khích tạo môi trường ảo (Virtual Environment) để tránh xung đột. Mở Terminal/Command Prompt tại thư mục dự án và chạy lệnh sau để tự động cài đặt các thư viện cần thiết (FastAPI, Transformers, PyTorch, Pillow,...) trong file requirements.txt:
```bash
pip install -r requirements.txt
```
### Trên Google Collab/ Jupyter Notebook
* Nếu chạy trên nền tảng đám mây, bạn cần thêm dấu chấm than (!) phía trước lệnh. Chạy đoạn code sau trong một ô (cell) mới:
```bash
!pip install fastapi uvicorn nest-asyncio python-multipart transformers torch pillow omegaconf requests
```

## 4. Hướng dẫn chạy chương trình
### Trên máy cá nhân (Local)
* **Đảm bảo cấu hình đúng đường dẫn mô hình trong file config.yaml:** Nếu chạy dưới local thì ta download xong và chạy nếu đã download về thì ta trích đường dẫn đến các file json của model. Mở Terminal tại thư mục chứa file main.py và khởi chạy Server bằng lệnh:
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
* Sau khi Server khởi động thành công, hệ thống sẽ chạy tại địa chỉ: http://127.0.0.1:8000.
### Trên Google Collab/ Jupyter Notebook
* Sau khi cài đặt thư viện chỉ cần thực hiện chạy lần lượt từ trên xuống các khối lệnh trong file API_Lab1.ipynb bao gồm:
  * Create Config File (Tệp chứa đường dẫn mô hình)
  * Build Model (Định nghĩa Class cho mô hình, thiết lập logic cho các hàm tải và chạy model)
  * Initialize Model (Kết nối mạng và tải mô hình BLIP về máy, nạp trực tiếp lên GPU của Collab)
  * Initialize API (Dựng máy chủ Web bằng FastAPI, tạo các cổng giao tiếp (như /generate), thiết lập các bước bắt lỗi người dùng và khởi chạy luồng ngầm (threading) để Server hoạt động mà không làm treo Colab.)

## 5. Hướng dẫn gọi API và ví dụ request/response

Hệ thống cung cấp Endpoint chính để xử lý ảnh tại đường dẫn `/generate` thông qua phương thức `POST`. Dưới đây là cách gọi API bằng thư viện `requests` của Python trên hai môi trường khác nhau:

### Gọi API trên máy cá nhân (Local)
* Khi chạy trên máy tính, Server sẽ mở ở địa chỉ cục bộ (localhost) thông qua chạy file `main.py` sau đó ta chạy file `test_api.py` với hình ảnh có sẵn nằm trong thư mục

### Gọi API trên Google Colab / Jupyter Notebook
* Sử dụng link ảnh có đường dẫn URL và dán vào để chọn ra ảnh cần phân tích
* Khi chạy local trên Colab, ta chỉ cần chạy ô nằm trong mục Call Local API
* Khi chạy trên Colab qua Pinggy, bạn cần thay đổi URL thành đường link Public mà Pinggy đã cung cấp và chạy ô nằm trong mục Call Public API có trên file API_Lab1.ipynb

### Có 3 Endpoint như sau:

### 1. **GET / :** Là endpoint cơ bản kiểm tra Server chạy hay chưa
* **Request mẫu (cURL)**
```bash
curl -X GET http://127.0.0.1:8000/
```

* **Response mẫu (JSON)**
```json
{
  "name": "BLIP Image Captioning API",
  "version": "1.0.0",
  "description": "API phục vụ mô hình BLIP sinh mô tả hình ảnh."
}
```

### 2. **GET /health :** Dùng để xem mô hình BLIP đã được load thành công vào bộ nhớ (RAM/VRAM) và sẵn sàng nhận ảnh chưa.
* **Request mẫu(cURL)**
```bash
curl -X GET http://127.0.0.1:8000/health
```

* **Response mẫu (JSON)**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cpu"
}
```

### 3. **POST /generate :** Đây là chức năng chính. Do dùng mô hình BLIP, server sẽ nhận một file ảnh và trả về một câu text mô tả nội dung bức ảnh đó.
* **Request mẫu(cURL)**
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_test1.jpg"
```

* **Response mẫu (JSON)**
```json
{
  "success": true,
  "filename": "sample_test1.jpg",
  "caption": "iron man vs captain america",
  "processing_time_seconds": 18.94
}
```

* **Reponse mẫu khi thất bại** (Status Code: 400 hoặc 422)
```json
{
  "success": false,
  "error": "Invalid file format. Please upload a valid image (JPEG/PNG)."
}
```


## Cấu trúc thư mục dự án
```text
Image-Captioning-Project/
│
├── main.py              # Mã nguồn chính của Server FastAPI và Class Model
├── test_api.py          # Script tự động kiểm thử các Endpoints bằng requests
├── config.yaml          # File cấu hình chứa đường dẫn lưu model
├── requirements.txt     # Danh sách các thư viện Python cần thiết
├── README.md            # Tài liệu hướng dẫn sử dụng 
├── API_Lab1.ipynb       # Notebook thử nghiệm model trên Google Collab, để sử dụng GPU T4
├── sample_test.jpg      # Ảnh mẫu dùng để kiểm thử hệ thống
├── sample_test1.jpg     # Ảnh mẫu dùng để kiểm thử hệ thống
└── Video_demo.mp4       # Video demo hệ thống
```

## Video Demo:

https://github.com/user-attachments/assets/c38d618b-ac0c-4d65-bf5b-d21c184d568e

