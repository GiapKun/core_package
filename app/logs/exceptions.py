from app.core.exceptions import ErrorCode as CoreErrorCode, CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def InvalidCollection(collection_name):
        return CustomException(
            type="logs/warning/collection",
            status=400,
            title="Bad Request.",
            detail=f"Collection {collection_name} does not exist in database.",
        )
