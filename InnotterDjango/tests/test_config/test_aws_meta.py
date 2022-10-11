from InnotterDjango.aws_metaclass import AWSMeta
import pytest


pytestmark = pytest.mark.django_db


class TestAWSMeta:
    def test_aws_meta_new(self):
        with pytest.raises(Exception):
            AWSMeta.__new__(..., '', (), {})
