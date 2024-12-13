from fastapi import Request
from domains.authentication.jwt import JWTHandler

class AuthenticationService:
    """Service for authentication and authorization."""

    def __init__(self, jwt_handler: JWTHandler, public_apis: list[str]):
        self.jwt_handler = jwt_handler
        self.public_apis = public_apis

    async def check_public_api(self, request: Request) -> bool:
        """Checks if the request is for a public API."""
        api_path = request.url.path
        return api_path in self.public_apis
