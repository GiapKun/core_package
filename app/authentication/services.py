from fastapi import Request
from app.authentication.jwt import JWTHandler
from app.authentication.exceptions import ErrorCode as AuthErrorCode

class AuthenticationService:
    """Service for authentication and authorization."""

    def __init__(self, jwt_handler: JWTHandler, public_apis: list[str]):
        self.jwt_handler = jwt_handler
        self.public_apis = public_apis

    async def check_public_api(self, request: Request) -> bool:
        """
        Checks if the request is for a public API.

        Args:
            request (Request): The FastAPI request object.

        Returns:
            bool: True if the API is public, False otherwise.
        """
        api_path = request.url.path
        return api_path in self.public_apis

    async def validate_token(self, auth_header: str) -> dict:
        """
        Validates a JWT token from the Authorization header.

        Args:
            auth_header (str): The Authorization header containing the Bearer token.

        Returns:
            dict: The decoded payload if the token is valid.

        Raises:
            CustomException: Specific authentication errors based on token validation.
        """
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthErrorCode.Forbidden()

        # Extract the token after "Bearer "
        token = auth_header.split(" ")[1]

        # Validate the token using JWTHandler
        return await self.jwt_handler.validate_access_token(token)


    async def check_api_access(self, request: Request) -> dict | None:
        """
        Checks if an API is public or validates the token for private APIs.

        Args:
            request (Request): The FastAPI request object.

        Returns:
            dict | None: The user payload for private APIs, or None for public APIs.

        Raises:
            AuthErrorCode.Forbidden: If the API is private and the token is invalid.
        """
        # Check if the API is public
        if await self.check_public_api(request):
            return None

        # Get the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        return await self.validate_token(auth_header)
