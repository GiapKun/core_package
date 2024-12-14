from dependency_injector import containers, providers
import logging
from core.logger import setup_logger
from database.session import DatabaseEngine
from database.crud import BaseCRUD
from authentication.jwt import JWTHandler
from authentication.services import AuthenticationService
from core.services import BaseServices
from core.controllers import BaseControllers

class CoreContainer(containers.DeclarativeContainer):
    """Core Dependency Injection Container"""

    # Configurations
    config = providers.Configuration()


    config.database_url.from_env("DATABASE_URL", default="mongodb://localhost:27020/")
    config.database_name.from_env("DATABASE_NAME", default="app")
    config.secret_key.from_env("SECRET_KEY", default="FoAG3Gzu7eQ0/7KVQ4UnY0bIeM1euUm8T4tGdn04/XUnsWlEoORpB2DRKtL6Zxn9RjhpucHrRi3yqIv4dyNKrQ==")
    config.algorithm.from_env("ALGORITHM", default="HS512")
    config.access_token_expire_days.from_env("ACCESS_TOKEN_EXPIRE_DAYS", default=7)
    config.logging.level.app.from_env("LOG_LEVEL_APP", default=logging.INFO)
    config.logging.level.request.from_env("LOG_LEVEL_REQUEST", default=logging.DEBUG)
    config.logging.level.database.from_env("LOG_LEVEL_DATABASE", default=logging.WARNING)


    # Database Engine
    database_engine = providers.Singleton(DatabaseEngine, database_url=config.database_url, database_name=config.database_name)
    # CRUD Provider
    example_crud = providers.Factory(BaseCRUD, database_engine=database_engine.provided.database, collection="example_collection")

    # CRUD Provider
    crud_factory = providers.Factory(BaseCRUD, database_engine=database_engine.provided.database)

    # Service Provider
    service_factory = providers.Factory(BaseServices)

    # Controller Provider
    controller_factory = providers.Factory(BaseControllers)


    jwt_handler = providers.Singleton(JWTHandler, secret_key=config.secret_key, algorithm=config.algorithm, access_token_expire_days=config.access_token_expire_days)
    auth_service = providers.Factory(AuthenticationService, jwt_handler=jwt_handler, public_apis=config.public_apis)


    # Logger Providers
    app_logger = providers.Singleton(setup_logger, name="app", level=config.logging.level.app)
    request_logger = providers.Singleton(setup_logger, name="request", level=config.logging.level.request)
    db_logger = providers.Singleton(setup_logger, name="database", level=config.logging.level.database,)