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
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
* Sau khi Server khởi động thành công, hệ thống sẽ chạy tại địa chỉ: http://127.0.0.1:8000.
### Trên Google Collab/ Jupyter Notebook
* Sau khi cài đặt thư viện chỉ cần thực hiện chạy lần lượt từ trên xuống các khối lệnh trong file API_Lab1.ipynb

## 5. Hướng dẫn gọi API và ví dụ request/response

Hệ thống cung cấp Endpoint chính để xử lý ảnh tại đường dẫn `/generate` thông qua phương thức `POST`. Dưới đây là cách gọi API bằng thư viện `requests` của Python trên hai môi trường khác nhau:

### Gọi API trên máy cá nhân (Local)
* Khi chạy trên máy tính, Server sẽ mở ở địa chỉ cục bộ (localhost). Chạy file `test_api.py`

### Gọi API trên Google Colab / Jupyter Notebook
* Khi chạy local trên Colab, ta chỉ cần chạy ô nằm trong mục Call Local API
* Khi chạy trên Colab qua Pinggy, bạn cần thay đổi URL thành đường link Public mà Pinggy đã cung cấp và chạy ô nằm trong mục Call Public API có trên file API_Lab1.ipynb


## 📂 Cấu trúc thư mục dự án
```text
Image-Captioning-Project/
│
├── main.py              # Mã nguồn chính của Server FastAPI và Class Model
├── test_api.py          # Script tự động kiểm thử các Endpoints bằng requests
├── config.yaml          # File cấu hình chứa đường dẫn lưu model
├── requirements.txt     # Danh sách các thư viện Python cần thiết
├── README.md            # Tài liệu hướng dẫn sử dụng 
├── API_Lab1.ipynb       # Notebook thử nghiệm model trên Google Collab, để sử dụng GPU T4
└── sample_test.jpg      # Ảnh mẫu dùng để kiểm thử hệ thống
└── sample_test1.jpg     # Ảnh mẫu dùng để kiểm thử hệ thống
