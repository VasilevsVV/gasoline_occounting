import unittest
from unittest.mock import patch
from business_logic import GasolineTable
from entities import Trip
from serialize import Serialize as sr


class BusinessLogicTests(unittest.TestCase):
    """Module with tests for business logic."""

    def setUp(self):
        self.gas = GasolineTable(test=True)

    def test_load(self):
        self.gas.load("test")
        self.assertEqual([self.gas.trips_table, self.gas.trips_ids],
                         [{}, 0])

    def test_name(self):
        self.assertEqual(self.gas.current_table_name(), "test")

    @staticmethod
    def make_filled_table():
        gas = GasolineTable(test=True)
        gas.add_trip(100, 200, 50)
        gas.add_trip(125, 300, 88)
        return gas

    @staticmethod
    def make_empty_table():
        return GasolineTable(test=True)

    @patch('serialize.Serialize.dump')
    def test_dump(self, dump):
        gas = BusinessLogicTests.make_empty_table()
        gas.set_serialize(sr.json)
        gas.dump()
        dump.assert_called_with('test', [{}, 0], sr.json)
        gas.set_new_name("test1")
        gas.dump()
        dump.assert_called_with('test1', [{}, 0], sr.json)

    @staticmethod
    def get_yaml():
        return 'yaml'

    @patch('business_logic.GasolineTable.__probe_config__')
    def test_init(self, probe):
        probe.side_effect = lambda: 'picle'
        gas = GasolineTable(test=True)
        self.assertEqual(gas.get_serialize(), sr.pickle)
        probe.side_effect = lambda: 'yaml'
        gas = GasolineTable(test=True)
        self.assertEqual(gas.get_serialize(), sr.yaml)
        probe.side_effect = lambda: 'json'
        gas = GasolineTable(test=True)
        self.assertEqual(gas.get_serialize(), sr.json)

    @patch('serialize.Serialize.delete')
    def test_delete(self, delete):
        gas = BusinessLogicTests.make_filled_table()
        gas.set_serialize(sr.yaml)
        gas.delete()
        delete.assert_called_with('test', sr.yaml)
        gas.set_serialize(sr.pickle)
        gas.delete("test1")
        delete.assert_called_with('test1', sr.pickle)


if __name__ == "__main__":
    unittest.main()
