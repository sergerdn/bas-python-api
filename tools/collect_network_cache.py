import asyncio
import codecs
import os.path

from bas_client import BasClient
from tools import ABS_PATH, get_tr_options


async def main():
    dest_filename = os.path.join(ABS_PATH, "tests", "fixtures", "network", "collected.json")
    tr_options = get_tr_options()
    client = BasClient(transport_options=tr_options)

    await client.setup()
    await client.network.cache_mask_allow(mask="*")

    urls = [
        "https://www.google.com/?hl=en" "https://en.wikipedia.org/wiki/Main_Page",
        "https://en.wikipedia.org/w/index.php?title=Special:UserLogin&returnto=Main+Page",
        "https://www.bing.com/",
        "https://yandex.com/",
    ]
    for url in urls:
        await client.browser.load(url)
        await client.waiters.wait_full_page_load()

    data = await client.run_function_thread("_basNetworkGetAllItemsFromCache", {"mask": "*"})
    await client.close()

    with codecs.open(dest_filename, "w", "utf-8") as fp:
        fp.write(str(data))


if __name__ == "__main__":
    asyncio.run(main())
