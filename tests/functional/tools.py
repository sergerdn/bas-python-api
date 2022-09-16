import asyncio
import shutil
import time
from io import StringIO

import yaml
from lxml import etree

parser = etree.HTMLParser()


async def clean_dir_async(dir_path):
    for _ in range(0, 60):
        try:
            shutil.rmtree(dir_path)
        except PermissionError:
            await asyncio.sleep(1)
            continue
        except FileNotFoundError:
            break

    return True


def clean_dir(dir_path):
    for _ in range(0, 60):
        try:
            shutil.rmtree(dir_path)
        except PermissionError:
            time.sleep(1)
            continue
        except FileNotFoundError:
            break

    return True


def json_from_httpbin(page_html: str):
    tree = etree.parse(StringIO(page_html), parser)
    page_data = tree.xpath("//pre")[0].text
    return yaml.load(page_data, Loader=yaml.UnsafeLoader)
