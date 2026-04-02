import requests
import os

# Trường hợp 1: Chạy Local (Mặc định)
BASE_URL = "http://127.0.0.1:8000"

# Trường hợp 2: Chạy Public 
# BASE_URL = "http://xxxx-xxx.a.free.pinggy.link" (Thay thế bằng URL đã lấy được từ Pinggy)

# Tên file ảnh dùng để kiểm thử (Đảm bảo file này có tồn tại trong cùng thư mục)
IMAGE_TO_TEST = "sample_test1.jpg"

# Định nghĩa các Endpoint cần kiểm thử
def test_get_root():
    """Kiểm tra Endpoint giới thiệu hệ thống"""
    print("\n--- Kiểm thử GET / (Thông tin hệ thống) ---")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Mã trạng thái: {response.status_code}")
        print("Kết quả:", response.json())
    except Exception as e:
        print(f"Không thể kết nối tới Server: {e}")

def test_get_health():
    """Kiểm tra trạng thái sẵn sàng của mô hình AI"""
    print("\n--- Kiểm thử GET /health (Trạng thái AI) ---")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Mã trạng thái: {response.status_code}")
        print("Kết quả:", response.json())
    except Exception as e:
        print(f"Lỗi kết nối: {e}")

def test_post_generate():
    """Kiểm tra chức năng chính: Sinh mô tả cho ảnh"""
    print(f"\n--- Kiểm thử POST /generate (Xử lý hình ảnh) ---")
    
    # 1. Kiểm tra file cục bộ trước khi gửi
    if not os.path.exists(IMAGE_TO_TEST):
        print(f"Lỗi: Không tìm thấy file '{IMAGE_TO_TEST}'. Vui lòng chuẩn bị một ảnh để test.")
        return

    try:
        url = f"{BASE_URL}/generate"
        
        with open(IMAGE_TO_TEST, "rb") as f:
            files = {"file": (IMAGE_TO_TEST, f, "image/jpeg")}
            print(f"Đang gửi ảnh '{IMAGE_TO_TEST}' tới {url}...")
            response = requests.post(url, files=files)
        
        print(f"Mã trạng thái: {response.status_code}")
        if response.status_code == 200:
            print(" Thành công! Kết quả:")
            print(response.json())
        else:
            print("Server trả về lỗi:")
            print(response.json())
            
    except Exception as e:
        print(f"Lỗi trong quá trình gửi request: {e}")

if __name__ == "__main__":
    print("=== Tiến hành kiểm tra ===")
    test_get_root()
    test_get_health()
    test_post_generate()
    print("\n=== Kết thúc kiểm tra ===")