from unittest import TestCase
from src.lime import Serializable


class SerializableTest(TestCase):

    def test_normalize_key(self):
        # arrange
        node_key = 'from_n'
        target = self.get_target()

        # act
        result = target.normalize_key(node_key)

        # assert
        self.assertEquals(result, 'from')

    def get_target(self):
        return Serializable()
