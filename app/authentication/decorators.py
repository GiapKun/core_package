import functools
from app.authentication.exceptions import ErrorCode as AuthErrorCode

def access_control(admin: bool = False):
    """Decorator for role-based access control."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("user")  # Assume user is injected in request
            if admin and user.get("user_type") != "admin":
                raise AuthErrorCode.Forbidden()
            return await func(*args, **kwargs)
        return wrapper
    return decorator
