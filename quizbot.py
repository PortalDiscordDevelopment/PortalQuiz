import traceback

import aiohttp
import aiosqlite
from PortalUtils import Bot

from schemas import schemas


class QuizBot(Bot):
    """
    Main bot class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db: aiosqlite.Connection
        self.session: aiohttp.ClientSession
        self.version = 2.1

    async def start(self, *args, **kwargs):
        async with aiosqlite.connect("data.db") as db:
            self.db = db
            for schema in schemas:
                try:
                    await db.execute(schema)
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)
            await super().start(*args, **kwargs)
