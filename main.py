import torch
import io
import time  
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse # Thêm import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image, UnidentifiedImageError
from omegaconf import OmegaConf
import uvicorn


class ImageCaptioningModel:
    def __init__(self, config_path):
        # Đọc cấu hình từ file yaml
        self.config = OmegaConf.load(config_path)

        # Kiểm tra thiết bị CUDA hoặc CPU do model có thể khá nặng
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Hệ thống đang sử dụng thiết bị tính toán: {self.device.upper()}")
        save_directory = "C:/AI_Models/HuggingFace_Cache"

        # Tải Processor và Model từ Hugging Face
        print(f"Đang tải mô hình từ Hugging Face vào bộ nhớ với đường dẫn {save_directory}")
        self.processor = BlipProcessor.from_pretrained(self.config.model_path,cache_dir=save_directory)
        self.model = BlipForConditionalGeneration.from_pretrained(self.config.model_path,cache_dir=save_directory).to(self.device)
        print("Tải mô hình thành công và đã sẵn sàng!")

    def predict(self, image: Image.Image):
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            out = self.model.generate(**inputs)
        caption = self.processor.decode(out[0], skip_special_tokens=True)
        return caption

# Khởi tạo mô hình
app = FastAPI(title="Image Captioning API")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Đảm bảo file config.yaml tồn tại trước khi khởi tạo
def ensure_config():
    import os
    if not os.path.exists("config.yaml"):
        with open("config.yaml", "w") as f:
            f.write('model_path: "Salesforce/blip-image-captioning-base"')

ensure_config()
classifier = ImageCaptioningModel("./config.yaml")

# Định nghĩa các Endpoint API
@app.get("/")
def read_root():
    "Endpoint giới thiệu hệ thống"
    return {
        "name": "BLIP Image Captioning API",
        "version": "1.0.0",
        "description": "API phục vụ mô hình BLIP sinh mô tả hình ảnh."
    }

@app.get("/health")
def health_check():
    """Endpoint kiểm tra trạng thái sẵn sàng của mô hình"""
    if classifier.model is not None:
        return {
            "status": "healthy", 
            "model_loaded": True, 
            "device": classifier.device
        }
    raise HTTPException(status_code=503, detail="Hệ thống chưa sẵn sàng.")

@app.post("/generate")
async def generate_caption(file: UploadFile = File(...)):
    """Xử lý ảnh và sinh caption"""
    start_time = time.time()
    
    # Kiểm tra sự tồn tại của file
    if not file.filename:
        return JSONResponse(
            status_code=400, 
            content={"success": False, "error": "Lỗi: Chưa đính kèm file ảnh."}
        )

    # Kiểm tra định dạng file
    if not file.content_type.startswith("image/"):
        return JSONResponse(
            status_code=400, 
            content={"success": False, "error": "Invalid file format. Please upload a valid image (JPEG/PNG)."}
        )

    try:
        image_data = await file.read()

        # Kiểm tra tính toàn vẹn của ảnh
        try:
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
        except UnidentifiedImageError:
            return JSONResponse(
                status_code=400, 
                content={"success": False, "error": "Lỗi dữ liệu: File ảnh bị hỏng hoặc không hỗ trợ."}
            )

        # Thực hiện dự đoán
        caption = classifier.predict(image)
        processing_time = round(time.time() - start_time, 2)
        return {
            "success": True,
            "filename": file.filename,
            "caption": caption,
            "processing_time_seconds": processing_time
        }

    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={"success": False, "error": f"Lỗi hệ thống trong quá trình suy luận: {str(e)}"}
        )

# Thực thi
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)