import codecs
import glob
import os.path
from typing import List

import pydantic
import yaml

from bas_client.models import Cookie, Cookies
from bas_client.models.network import NetworkCacheEntry


class TestModels:
    def test_cookie_model(self, fixtures_dir):
        fixtures_dir = os.path.join(fixtures_dir, "cookies")
        assert os.path.exists(fixtures_dir)
        assert os.path.isdir(fixtures_dir)

        for filename in glob.glob(os.path.join(fixtures_dir, "*.json")):
            with codecs.open(filename, "r+", "utf-8") as fp:
                data = fp.read()

            data_obj = yaml.load(data, Loader=yaml.UnsafeLoader)
            for one in data_obj["cookies"]:
                try:
                    obj_model = Cookie(**one)
                except pydantic.error_wrappers.ValidationError as exc:
                    print(one)
                    raise ValueError(str(exc))

            obj_model = Cookies(**data_obj)
            assert len(obj_model.cookies) >= 1

    def test_network_model(self, fixtures_dir):
        fixtures_dir = os.path.join(fixtures_dir, "network")
        assert os.path.exists(fixtures_dir)
        assert os.path.isdir(fixtures_dir)

        for filename in glob.glob(os.path.join(fixtures_dir, "*.json")):
            with codecs.open(filename, "r+", "utf-8") as fp:
                data = fp.read()

            data_obj = yaml.load(data, Loader=yaml.UnsafeLoader)
            obj_model_cache: List[NetworkCacheEntry] = []
            for one in data_obj:
                try:
                    obj_model = NetworkCacheEntry(**one)
                except pydantic.error_wrappers.ValidationError as exc:
                    print(one)
                    raise ValueError(str(exc))

                obj_model_cache.append(obj_model)

            assert len(obj_model_cache) >= 1
