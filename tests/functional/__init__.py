import os


def test_api_basic_env_set(transport_options):
    assert transport_options.remote_script_name is not None
    assert transport_options.remote_script_user is not None
    assert transport_options.remote_script_password is not None
    assert transport_options.working_dir is not None
    assert os.path.exists(transport_options.working_dir) is True
