import os.path

import pytest

from bas_api import BasApi, RemoteTransportOptions


def test_api_basic_env_set(remote_script_name, remote_script_user, remote_script_password, working_dir):
    assert remote_script_name is not None
    assert remote_script_user is not None
    assert remote_script_password is not None
    assert working_dir is not None
    assert os.path.exists(working_dir) is True
    assert os.path.isdir(working_dir) is True


class TestApiBasic:
    @pytest.mark.asyncio
    async def test_api_basic(self, remote_script_name, remote_script_user, remote_script_password, working_dir):
        transport_options = RemoteTransportOptions(
            remote_script_name=remote_script_name,
            remote_script_user=remote_script_user,
            remote_script_password=remote_script_password,
            working_dir=working_dir,
        )
        api = BasApi(transport_options=transport_options)
        await api.set_up()
