from containers import CoreContainer
import asyncio

async def main():
    container = CoreContainer()

    # Resolve CRUD instance
    example_crud = container.example_crud()

    # Insert a document
    doc_id = await example_crud.save({"name": "John Doe", "status": "active"})
    print(f"Inserted document ID: {doc_id}")

    # Count documents again
    count = await example_crud.count_documents({})
    print(f"Document count after insert: {count}")


    # Resolve JWTHandler
    jwt_handler = container.jwt_handler()

    # Tạo token
    token = await jwt_handler.create_access_token(user_id="123", user_type="admin")
    print(f"Generated Token: {token}")

    # Xác thực token
    payload = await jwt_handler.validate_access_token(f"Bearer {token}")
    if payload:
        print(f"Token is valid: {payload}")
    else:
        print("Token is invalid or expired.")


if __name__ == "__main__":
    asyncio.run(main())
