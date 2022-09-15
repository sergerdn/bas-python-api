import asyncio
import shutil


async def clean_dir(dir_path):
    for _ in range(0, 60):
        try:
            shutil.rmtree(dir_path)
        except PermissionError:
            await asyncio.sleep(1)
            continue
        except FileNotFoundError:
            break

    return True
