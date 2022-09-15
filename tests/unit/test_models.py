import codecs
import glob
import os.path

import yaml

from bas_api.models import Cookies


class TestModels:
    def test_cookie_model(self, fixtures_dir):
        cookies_dir = os.path.join(fixtures_dir, "cookies")
        assert os.path.exists(cookies_dir)
        assert os.path.isdir(cookies_dir)
        for filename in glob.glob(os.path.join(cookies_dir, "*.json")):
            with codecs.open(filename, "r+", "utf-8") as fp:
                data = fp.read()

            data_json = yaml.load(data, Loader=yaml.UnsafeLoader)
            obj_model = Cookies(**data_json)
            assert len(obj_model.cookies) >= 1
