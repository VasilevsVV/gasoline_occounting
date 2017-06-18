import pickle as p
from json_serialize import JsonSerialize as js
import yaml
import utils


class Serialize:
    pickle = 1
    yaml = 2
    json = 3

    @staticmethod
    def file_name(method):
        home = utils.home_name()
        if method == Serialize.pickle:
            file = b'/.gas_storage.pickle'
        elif method == Serialize.yaml:
            file = b'/.gas_storage.yaml'
        else:
            file = b'/.gas_storage.json'
        print(file)
        return home + file

    @staticmethod
    def file_spec_w(method):
        if method == Serialize.pickle:
            return 'wb'
        else:
            return 'w'

    @staticmethod
    def file_spec_r(method):
        if method == Serialize.pickle:
            return 'rb'
        else:
            return 'r'

    @staticmethod
    def read_file(method):
        return open(Serialize.file_name(method),
                    Serialize.file_spec_r(method))

    @staticmethod
    def write_file(method):
        return open(Serialize.file_name(method),
                    Serialize.file_spec_w(method))

    @staticmethod
    def dump(table_name, data, method):
        table = Serialize.load_all(method)
        table[table_name] = data
        Serialize.dump_all(table, method)

    @staticmethod
    def dump_all(data, method):
        with Serialize.write_file(method) as f:
            if method == Serialize.pickle:
                p.dump(data, f)
            elif method == Serialize.yaml:
                yaml.dump(data, f)
            else:
                js.dump(data, f)
            f.close()

    @staticmethod
    def load_all(method):
        try:
            with Serialize.read_file(method) as f:
                if method == Serialize.pickle:
                    table = p.load(f)
                elif method == Serialize.yaml:
                    table = yaml.load(f)
                else:
                    table = js.load(f)
                f.close()
        except:
            table = {}
        if table is None:
            print('IT IS NONE')
            table = {}
        print(table)
        return table

    @staticmethod
    def load(table_name, method):
        table = Serialize.load_all(method)
        return table.get(table_name, [{}, 0])

    @staticmethod
    def delete(table_name, method):
        table = Serialize.load_all(method)
        try:
            table.pop(table_name)
            Serialize.dump_all(table, method)
            return True
        except:
            return False

