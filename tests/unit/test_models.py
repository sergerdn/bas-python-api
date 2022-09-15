import codecs
import glob
import os.path

import pydantic
import yaml

from bas_api.models import Cookie, Cookies


class TestModels:
    def test_cookie_model(self, fixtures_dir):
        cookies_dir = os.path.join(fixtures_dir, "cookies")
        assert os.path.exists(cookies_dir)
        assert os.path.isdir(cookies_dir)
        for filename in glob.glob(os.path.join(cookies_dir, "*.json")):
            with codecs.open(filename, "r+", "utf-8") as fp:
                data = fp.read()

            data_json = yaml.load(data, Loader=yaml.UnsafeLoader)
            for one in data_json["cookies"]:
                try:
                    obj_model = Cookie(**one)
                except pydantic.error_wrappers.ValidationError as exc:
                    print()
                    print(one)
                    raise exc

            obj_model = Cookies(**data_json)
            assert len(obj_model.cookies) >= 1
