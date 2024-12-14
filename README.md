# fastapi-micro-core

```
app/
├── **init**.py # File khởi tạo package
├── containers.py # Định nghĩa Dependency Injection container
│
├── domains/ # Các domain chính
│ ├── **init**.py
│ ├── authentication/ # Domain xác thực
│ │ ├── **init**.py
│ │ ├── decorators.py # Role-based Access Control
│ │ ├── exceptions.py # Exception cho authentication
│ │ ├── interfaces.py # Định nghĩa các interface cho domain
│ │ ├── services.py # Logic xử lý xác thực
│ │ ├── jwt.py # Xử lý JWT
│ ├── users/ # Domain người dùng
│ │ ├── **init**.py
│ │ ├── models.py # Các model liên quan đến người dùng
│ │ ├── services.py # Logic xử lý người dùng
│ │ ├── interfaces.py # Định nghĩa các interface cho domain
│ ├── database/ # Domain database
│ ├── **init**.py
│ ├── session.py # Quản lý phiên database (e.g., SQLAlchemy)
│ ├── models.py # Định nghĩa các model cơ sở dữ liệu chung
│
├── core/ # Thành phần lõi của package
│ ├── **init**.py
│ ├── settings.py # Cấu hình toàn cục
│ ├── exceptions.py # Các exception chung
│ ├── logger.py # Hỗ trợ logging
│
├── utils/ # Package chứa các hàm tiện ích
│ ├── **init**.py
│ ├── calculator.py # Hàm tính toán thời gian, số học
│ ├── converter.py # Hàm chuyển đổi định dạng dữ liệu
│ ├── validator.py # Hỗ trợ validate
│ ├── value.py # Hỗ trợ các giá trị data format
│
└── tests/ # Thư mục test
├── **init**.py
├── test_auth.py # Test cho domain authentication
├── test_users.py # Test cho domain users
```
