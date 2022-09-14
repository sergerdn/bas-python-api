from bas_api import BasApi, RemoteTransportOptions


def test_api_basic_env_set(remote_script_name, remote_script_user, remote_script_password):
    assert remote_script_name is not None
    assert remote_script_user is not None
    assert remote_script_password is not None


class TestApiBasic:
    def test_api_basic(self, remote_script_name, remote_script_user, remote_script_password):
        transport_options = RemoteTransportOptions(
            remote_script_name=remote_script_name,
            remote_script_user=remote_script_user,
            remote_script_password=remote_script_password,
        )
        api = BasApi(transport_options=transport_options)
        await api.set_up()
