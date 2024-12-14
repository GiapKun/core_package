from datetime import datetime
from jose import jwt
from utils import converter, calculator
from authentication.exceptions import ErrorCode as AuthErrorCode

class JWTHandler:
    """Handles JWT creation and validation."""

    def __init__(self, secret_key: str, algorithm: str, access_token_expire_days: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_days = access_token_expire_days

    async def create_access_token(self, user_id: str, user_type: str, extra_claims: dict = None) -> str:
        """
        Creates a JWT access token for the specified user.

        Args:
            user_id (str): The ID of the user for whom the token is being created.
            user_type (str): The type of the user (e.g., admin, customer).
            extra_claims (dict): Additional claims to include in the token.

        Returns:
            str: The encoded JWT access token.
        """
        expire = calculator.add_days_to_datetime(days=self.access_token_expire_days)
        expire_str = converter.convert_datetime_to_str(datetime_obj=expire)

        # Default claims
        to_encode = {
            "user_id": user_id,
            "user_type": user_type,
            "expire": expire_str
        }

        # Include extra claims if provided
        if extra_claims:
            to_encode.update(extra_claims)

        encoded_jwt = jwt.encode(claims=to_encode, key=self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def validate_access_token(self, token: str) -> dict:
        """
        Validates a JWT access token.

        Args:
            token (str): The JWT access token to be validated.

        Returns:
            dict: The decoded payload if the token is valid.

        Raises:
            CustomException: Specific authentication errors based on token validation.
        """
        try:
            # Decode token
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # Validate expiration
            datetime_obj = converter.convert_str_to_datetime(datetime_str=payload["expire"])
            if datetime.now() > datetime_obj:
                raise AuthErrorCode.TokenExpired()

            # Ensure user_id exists in payload
            if not payload.get("user_id"):
                raise AuthErrorCode.MissingUserId()

            return payload

        except jwt.JWTError:
            raise AuthErrorCode.InvalidToken()
