import asyncio
import logging

import pytest

from bas_client import BasClient


@pytest.fixture(scope="class", autouse=True)
def client(request, transport_options, event_loop: asyncio.AbstractEventLoop):
    api = BasClient(transport_options=transport_options, loop=event_loop)

    def fin():
        async def afin():
            logging.debug("teardown api....")
            await api.clean_up()

        event_loop.run_until_complete(afin())

    request.addfinalizer(fin)
    event_loop.run_until_complete(api.set_up())

    return api
