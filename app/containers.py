from dependency_injector import containers, providers
from domains.database.session import DatabaseEngine
from domains.database.crud import BaseCRUD
from domains.authentication.jwt import JWTHandler

class CoreContainer(containers.DeclarativeContainer):
    """Core Dependency Injection Container"""

    # Configurations
    config = providers.Configuration()
    config.database_url.from_env("DATABASE_URL", default="mongodb://localhost:27020/")
    config.database_name.from_env("DATABASE_NAME", default="app")

    # Database Engine
    database_engine = providers.Singleton(DatabaseEngine, database_url=config.database_url, database_name=config.database_name)

    # CRUD Provider
    example_crud = providers.Factory(
        BaseCRUD,
        database_engine=database_engine.provided.database,
        collection="example_collection"
    )


    config.secret_key.from_env("SECRET_KEY", default="FoAG3Gzu7eQ0/7KVQ4UnY0bIeM1euUm8T4tGdn04/XUnsWlEoORpB2DRKtL6Zxn9RjhpucHrRi3yqIv4dyNKrQ==")
    config.algorithm.from_env("ALGORITHM", default="HS512")
    config.access_token_expire_days.from_env("ACCESS_TOKEN_EXPIRE_DAYS", default=3)

    # JWT Handler
    jwt_handler = providers.Singleton(
        JWTHandler,
        secret_key=config.secret_key,
        algorithm=config.algorithm,
        access_token_expire_days=config.access_token_expire_days,
    )