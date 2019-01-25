import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

class TestPost:
    def test_init(self):
        obj = mixer.blend('catalog.User')
        assert obj.pk == 1, 'Should save an instance'

def test_init(self):
    obj = mixer.blend('catalog.User')
    assert obj.pk == 1, 'Should save an instance'

! pytest