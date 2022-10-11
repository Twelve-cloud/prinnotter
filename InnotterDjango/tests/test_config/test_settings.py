import InnotterDjango.settings
from imp import reload
import pytest
import os


pytestmark = pytest.mark.django_db


class TestSettings:
    def test_heroku_presence(self):
        os.environ['DYNO'] = 'True'
        reload(InnotterDjango.settings)
        assert InnotterDjango.settings.IS_HEROKU is True

        os.environ['DATABASE_URL'] = 'True'
        with pytest.raises(KeyError):
            reload(InnotterDjango.settings)
