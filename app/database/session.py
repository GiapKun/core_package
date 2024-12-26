from motor.motor_asyncio import AsyncIOMotorClient

class DatabaseEngine:
    """Database Engine class."""
    def __init__(self, database_url: str, database_name: str):
        self.client = AsyncIOMotorClient(database_url)
        self.database = self.client[database_name]

    def get_database(self):
        """Return the database instance."""
        return self.database
