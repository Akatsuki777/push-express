import asyncio
import os

from dotenv import load_dotenv


def grab_env_var(key):
    if not os.getenv(key):
        load_dotenv()

    return os.getenv(key)


async def background_loop(logger=None):
    import constants
    from services.check_draws import check_draw
    from services.push_notification import notify

    while True:
        is_draw = check_draw(logger)
        if is_draw:
            notify(is_draw)

        await asyncio.sleep(constants.TIMER)
