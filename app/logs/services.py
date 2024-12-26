import time
from io import BytesIO
from tempfile import SpooledTemporaryFile

from app.core.services import BaseServices
from app.database.crud import BaseCRUD
from app.utils import validator

from .exceptions import ErrorCode as LogErrorCode


class LogServices(BaseServices):
    def __init__(self, crud: BaseCRUD, service_name: str, owner_type: str = None) -> None:
        super().__init__(crud, service_name, owner_type)

    async def parse_response(self, response):
        result = {}
        result["headers"] = dict(response.headers)
        result["status_code"] = response.status_code
        try:
            result["body"] = response.json()
        except Exception:
            result["body"] = response.text

        return result

    async def save(self, request_id, request, response):
        domain = validator.check_domain(request["url"])
        response = await self.parse_response(response)
        data = {}
        data["request_id"] = request_id
        data["request"] = request
        data["response"] = response
        data["created_at"] = time.time()
        if data["request"].get("files"):
            if type(data["request"]["files"].get("file")) in [tuple, list]:
                data["request"]["files"]["file"] = [item for item in data["request"]["files"]["file"] if not isinstance(item, SpooledTemporaryFile) and not isinstance(item, BytesIO)]
        domain = "internal.requests" if not domain else domain
        await self.crud.set_collection(domain)
        await self.crud.save(data)

    async def check_collections(self, collection_name):
        if not await self.crud.check_collections(collection_name):
            raise LogErrorCode.InvalidCollection(collection_name)

    async def get_logs(self, collection_name, request_id, authorization, method, params):
        await self.crud.change_collection(collection_name)
        return await self.crud.get_logs(request_id, authorization, method, params.page, params.limit, params.sort, params.sorted.value)
