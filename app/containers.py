from dependency_injector import containers, providers
from app.database.session import DatabaseEngine
from app.database.crud import BaseCRUD
from app.authentication.jwt import JWTHandler
from app.authentication.services import AuthenticationService
from app.core.services import BaseServices
from app.core.controllers import BaseControllers
from app.logs.services import LogServices
from app.history.decorator import HistoryDecorators
from app.security.services import SecurityServices

class CoreContainer(containers.DeclarativeContainer):
    """Core Dependency Injection Container"""

    # Configurations
    config = providers.Configuration()
    
    # Engine app
    config.database_url.from_env("DATABASE_URL", default="mongodb://localhost:27020/")
    config.app_database_name.from_env("APP_DATABASE_NAME", default="app")
    engine_app = providers.Singleton(DatabaseEngine, database_url=config.database_url, database_name=config.app_database_name)
    
    # create a logger service
    config.logs_database_name.from_env("LOGS_DATABASE_NAME", default="logs")
    engine_logs = providers.Singleton(DatabaseEngine, database_url=config.database_url, database_name=config.logs_database_name)
    logs_crud = providers.Factory(BaseCRUD, database_engine=engine_logs.provided.database, collection="logs")
    log_services = providers.Factory(LogServices, crud=logs_crud, service_name="log services")

    # create a history decorator
    config.history_database_name.from_env("HISTORY_DATABASE_NAME", default="history")
    engine_history = providers.Singleton(DatabaseEngine, database_url=config.database_url, database_name=config.history_database_name)
    history_crud = providers.Factory(BaseCRUD, database_engine=engine_history.provided.database, collection="history")
    history_decorator = providers.Factory(HistoryDecorators, crud=history_crud)

    # create a authentication service
    config.secret_key.from_env("SECRET_KEY", default="...")
    config.algorithm.from_env("ALGORITHM", default="...")
    config.access_token_expire_days.from_env("ACCESS_TOKEN_EXPIRE_DAYS", default=7)
    jwt_handler = providers.Singleton(JWTHandler, secret_key=config.secret_key, algorithm=config.algorithm, access_token_expire_days=config.access_token_expire_days)
    auth_service = providers.Factory(AuthenticationService, jwt_handler=jwt_handler, public_apis=config.public_apis)

    # Add BaseServices as a provider
    base_services = providers.Factory(BaseServices)

    # Add BaseControllers as a provider
    base_controllers = providers.Factory(BaseControllers)