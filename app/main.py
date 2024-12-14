from containers import CoreContainer
import asyncio

async def main():
    container = CoreContainer()

    # # Resolve CRUD instance
    # example_crud = container.example_crud()
    # # Insert a document
    # doc_id = await example_crud.save({"name": "John Doe", "status": "active"})
    # print(f"Inserted document ID: {doc_id}")
    # # Count documents again
    # count = await example_crud.count_documents({})
    # print(f"Document count after insert: {count}")


    # # Resolve JWTHandler
    # jwt_handler = container.jwt_handler()
    # # Tạo JWT token
    # print("Step 1: Create Token")
    # token = await jwt_handler.create_access_token(user_id="123", user_type="admin")
    # print(f"Generated Token: {token}")

    # # Xác thực token
    # print("\nStep 2: Validate Token")
    # try:
    #     payload = await jwt_handler.validate_access_token(token)
    #     print(f"Validated Payload: {payload}")
    # except Exception as e:
    #     print(f"Validation failed: {e}")



    # # Resolve AuthenticationService
    # auth_service = container.auth_service()
    # # Kiểm tra quyền truy cập API
    # print("\nStep 3: Check API Access")
    # from fastapi import Request
    # from starlette.datastructures import Headers

    # # Giả lập request
    # headers = Headers({"Authorization": f"Bearer {token}"})
    # request = Request(scope={"type": "http", "headers": headers.raw, "path": "/protected"})

    # try:
    #     user_payload = await auth_service.check_api_access(request)
    #     print(f"User Payload: {user_payload}")
    # except Exception as e:
    #     print(f"API Access failed: {e}")

    # Lấy logger từ container
    # app_logger = container.app_logger()
    # request_logger = container.request_logger()
    # db_logger = container.db_logger()
    # app_logger.info("Starting the application")
    # request_logger.critical("Processing a request")
    # db_logger.warning("Executing a database operation")

    # Innit User
    user_crud = container.crud_factory(collection="users")
    # Tạo Service
    user_service = container.service_factory(service_name="user", crud=user_crud)
    # Tạo Controller
    user_controller = container.controller_factory(controller_name="user", service=user_service)

if __name__ == "__main__":
    asyncio.run(main())
