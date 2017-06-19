from io import StringIO, BytesIO
import unittest
import business_logic as bl
import serialize as sr
from json_serialize import JsonSerialize as js
import pickle
import json

class SerializeTests(unittest.TestCase):

    def setUp(self):
        table = bl.GasolineTable(test=True)
        table.add_trip(100, 200, 50)
        table.add_trip(200, 250, 70)
        # table.add_trip(50, 270, 110)
        self.data = [table.trips_table, table.trips_ids]
        self.output = None

    def test_pickle(self):
        """ test for pickle serialize. """
        output = pickle.dumps(self.data)
        self.output = BytesIO(output)
        result = pickle.load(self.output)
        self.assertEqual(self.data, result)

    def test_json(self):
        output = json.dumps(self.data, default=js.encode_trip)
        self.output = StringIO(output)
        extr_data = js.decode_tables(json.load(self.output))
        self.assertEqual(self.data, extr_data)

    def tearDown(self):
        self.output.close()

if __name__ == "__main__":
    unittest.main()