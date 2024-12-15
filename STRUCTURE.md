# fastapi-micro-core

```
app/
|    ├── **init**.py # File khởi tạo package
|    |
|    ├── authentication/ # Domain xác thực
|    │ ├── **init**.py
|    │ ├── decorators.py # Role-based Access Control
|    │ ├── exceptions.py # Exception cho authentication
|    │ ├── services.py # Logic xử lý xác thực
|    │ ├── jwt.py # Xử lý JWT
|    │
|    ├── core/ # Thành phần lõi của package
|    │ ├── **init**.py
|    │ ├── config.py # Cấu hình toàn cục
|    │ ├── controllers.py # Controller core
|    │ ├── exceptions.py # Các exception chung
|    │ ├── logger.py # Hỗ trợ logging
|    │ ├── schemas.py # Define commom depencies, PaginationParams
|    │ ├── services.py # Service core
|    │
|    |
|    ├── database/ # Domain database
|    │ ├── **init**.py
|    │ ├── session.py # Quản lý phiên database
|    │ ├── crud.py # Define crud method
|    |
|    ├── utils/ # Package chứa các hàm tiện ích
|    │ ├── **init**.py
|    │ ├── calculator.py # Hàm tính toán thời gian, số học
|    │ ├── converter.py # Hàm chuyển đổi định dạng dữ liệu
|    │ ├── validator.py # Hỗ trợ validate
|    │ ├── value.py # Hỗ trợ các giá trị data format
|
├── containers.py # Định nghĩa Dependency Injection container
├── requirements.py # Python lib
├── main.py # Test
```
