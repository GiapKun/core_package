import functools
import inspect

from . import config, models


class HistoryDecorators:
    def __init__(self, crud) -> None:
        self.crud = crud

    async def get_different_data(self, old_data: dict, new_data: dict):
        if new_data is None:
            return {}
        differences = {}
        if old_data is None:
            old_data = {}
        if isinstance(old_data, (str, int, float)) or isinstance(new_data, (str, int, float)):
            if old_data != new_data:
                return new_data
            else:
                return None
        # Duyệt qua tất cả các khóa trong old_data và new_data
        for key in set(old_data.keys()).union(new_data.keys()):
            old_value = old_data.get(key)
            new_value = new_data.get(key)

            if isinstance(old_value, list) and isinstance(new_value, list):
                list_differences = []

                max_length = max(len(old_value), len(new_value))
                for i in range(max_length):
                    old_item = old_value[i] if i < len(old_value) else None
                    new_item = new_value[i] if i < len(new_value) else None

                    sub_differences = await self.get_different_data(old_item, new_item)
                    if sub_differences:
                        list_differences.append(sub_differences)

                if list_differences:
                    differences[key] = list_differences

            elif isinstance(old_value, dict) and isinstance(new_value, dict):
                sub_differences = await self.get_different_data(old_value, new_value)
                if sub_differences and key not in config.FIELD_NOT_LOG:
                    differences[key] = sub_differences

            elif old_value != new_value and key not in config.FIELD_NOT_LOG:
                differences[key] = new_value

        return differences

    async def clear_field_not_log(self, data):
        new_data = {}
        for key, value in data.items():
            if key not in config.FIELD_NOT_LOG:
                new_data[key] = value
        return new_data

    async def save_action_history(self, name, action, self_instance, document_id, function_caller, commons, new_data=None, old_data=None):
        module = self_instance.get_module_name()

        if action == "update" and old_data:
            new_data_copy = new_data.copy()
            new_data = await self.get_different_data(old_data=old_data, new_data=new_data)
            old_data = await self.get_different_data(old_data=new_data_copy, new_data=old_data)
        if action == "create" and new_data:
            new_data = await self.clear_field_not_log(data=new_data)

        # Create log
        data_save = {}
        data_save["document_id"] = document_id
        data_save["name"] = name
        data_save["action"] = action
        data_save["type"] = module + "/" + function_caller.replace("_", "-")
        data_save["new_data"] = new_data
        data_save["old_data"] = old_data
        data_save["created_at"] = self_instance.get_current_timestamp()
        data_save["created_by"] = self_instance.get_current_user(commons=commons)

        data_save = models.History(**data_save).model_dump()
        await self.crud.set_collection(module)
        await self.crud.save(data_save)

    def log_create_action_history(self, name: str):
        def decorator_log(func):
            @functools.wraps(func)
            async def wrapper_log_history(*args, **kwargs):
                # Call the original function
                result = await func(*args, **kwargs)
                try:
                    # Extract information from args and kwargs
                    self_instance = args[0]
                    data = kwargs.get("data", {}).copy()
                    commons = kwargs.get("commons")
                    function_caller = func.__name__

                    # Update log from new data
                    document_id = result.get("_id")
                    if not data:
                        data = await self_instance.get_by_id(_id=document_id, ignore_error=True)

                    await self.save_action_history(name=name, action="create", self_instance=self_instance, document_id=document_id, function_caller=function_caller, commons=commons, new_data=data)
                except Exception:
                    pass
                return result

            return wrapper_log_history

        return decorator_log

    def log_update_action_history(self, name: str, id_name: str = "_id"):
        def decorator_log(func):
            @functools.wraps(func)
            async def wrapper_log_history(*args, **kwargs):
                # Extract information from args and kwargs
                self_instance = args[0]

                document_id = kwargs.get(id_name)
                commons = kwargs.get("commons")
                current_item = None
                if document_id:
                    current_item = await self_instance.get_by_id(_id=document_id, commons=commons, ignore_error=True)

                # Call the original function
                result = await func(*args, **kwargs)
                try:
                    function_caller = inspect.stack()[1].function
                    if not document_id:
                        document_id = result.get("_id")
                    new_data = await self_instance.get_by_id(_id=document_id, commons=commons, ignore_error=True)
                    # Update log from new data
                    await self.save_action_history(name=name, action="update", self_instance=self_instance, document_id=document_id, function_caller=function_caller, commons=commons, new_data=new_data, old_data=current_item)
                except Exception:
                    pass
                return result

            return wrapper_log_history

        return decorator_log

    def log_delete_action_history(self, name: str, id_name: str = "_id"):
        def decorator_log(func):
            @functools.wraps(func)
            async def wrapper_log_history(*args, **kwargs):
                # Call the original function
                result = await func(*args, **kwargs)
                try:
                    # Extract information from args and kwargs
                    self_instance = args[0]
                    commons = kwargs.get("commons")
                    function_caller = inspect.stack()[1].function

                    # Update log from new data
                    document_id = kwargs.get(id_name)
                    await self.save_action_history(name=name, action="delete", self_instance=self_instance, document_id=document_id, function_caller=function_caller, commons=commons)
                except Exception:
                    pass
                return result

            return wrapper_log_history

        return decorator_log

    def log_active_or_renew_service_action_history(self, name: str, id_name: str = "_id"):
        """
        Decorator to log the history of service activation or renewal actions for a specified duration.

        This decorator wraps around a function that performs actions related to activating or renewing a service.
        It logs the action history with a specified name and billing cycle duration, capturing both the state before
        and after the action.

        Args:
            name (str): The name of the service action to log.
            id_name (str, optional): The key name for the document ID in the kwargs. Defaults to "_id".

        Returns:
            function: A decorator function that wraps the target function to include action logging.

        Usage:
            @log_active_or_renew_service_action_history(name="Activate Service")
            async def activate_service(self, *args, **kwargs):
                # Function implementation
                pass

        """

        def decorator_log(func):
            @functools.wraps(func)
            async def wrapper_log_history(*args, **kwargs):
                # Extract information from args and kwargs
                self_instance = args[0]

                document_id = kwargs.get(id_name)
                commons = kwargs.get("commons")
                billing_cycle = kwargs.get("billing_cycle")
                new_name = f"{name} {billing_cycle} tháng"
                current_item = None
                if document_id:
                    current_item = await self_instance.get_by_id(_id=document_id, commons=commons, ignore_error=True)

                # Call the original function
                result = await func(*args, **kwargs)
                try:
                    function_caller = inspect.stack()[1].function
                    new_data = await self_instance.get_by_id(_id=document_id, commons=commons, ignore_error=True)
                    # Update log from new data
                    await self.save_action_history(name=new_name, action="update", self_instance=self_instance, document_id=document_id, function_caller=function_caller, commons=commons, new_data=new_data, old_data=current_item)
                except Exception as e:
                    print("History failed: ", e)
                return result

            return wrapper_log_history

        return decorator_log