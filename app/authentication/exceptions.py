from app.core.exceptions import ErrorCode as CoreErrorCode, CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def TokenExpired():
        return CustomException(
            type="auth/error/token_expired",
            status=401,
            title="Token Expired",
            detail="The token has expired. Please log in again.",
        )

    @staticmethod
    def InvalidToken():
        return CustomException(
            type="auth/error/invalid_token",
            status=401,
            title="Invalid Token",
            detail="The provided token is invalid.",
        )

    @staticmethod
    def MissingUserId():
        return CustomException(
            type="auth/error/missing_user_id",
            status=401,
            title="Invalid Token Payload",
            detail="The token payload is missing the user_id field.",
        )

    @staticmethod
    def Forbidden():
        return CustomException(type="auth/error/forbidden", status=403, title="Forbidden.", detail="You do not have permission to access this resource.")