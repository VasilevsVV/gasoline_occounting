import pickle as p
from json_serialize import JsonSerialize as js
import yaml
import utils


class Serialize:
    """Module for serializations."""
    pickle = 1
    yaml = 2
    json = 3

    @staticmethod
    def file_name(method):
        """Generates file name based on os variables
        and method of serialization.
        Args:
            method: Method of serialization."""
        home = utils.home_name()
        if method == Serialize.pickle:
            file = b'/.gas_storage.pickle'
        elif method == Serialize.yaml:
            file = b'/.gas_storage.yaml'
        else:
            file = b'/.gas_storage.json'
        return home + file

    @staticmethod
    def file_spec_w(method):
        """Returns file specification for write file
         based on method of serialization.
        Args:
            method:Method of serialization."""
        if method == Serialize.pickle:
            return 'wb'
        else:
            return 'w'

    @staticmethod
    def file_spec_r(method):
        """Returns file specification for read file
        based on method of serialization.
        Args:
            method:Method of serialization."""
        if method == Serialize.pickle:
            return 'rb'
        else:
            return 'r'

    @staticmethod
    def read_file(method):
        """resturns a read file instance.
        Args:
            method:Method of serialization."""
        return open(Serialize.file_name(method),
                    Serialize.file_spec_r(method))

    @staticmethod
    def write_file(method):
        """resturns a write file instance.
        Args:
            method:Method of serialization."""
        return open(Serialize.file_name(method),
                    Serialize.file_spec_w(method))

    @staticmethod
    def dump(table_name, data, method):
        """Dumps a table to a storage by name.
        Args:
            table_name:Name of a table to dump.
            data:Data
            method:Method of serialization."""
        table = Serialize.load_all(method)
        table[table_name] = data
        Serialize.dump_all(table, method)

    @staticmethod
    def dump_all(data, method):
        """Dumps a data to storage.
        Args:
            data:Data
            method:Method of serialization."""
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
        """Loads a data from storage.
        Args:
            method:Method of loading"""
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
            table = {}
        return table

    @staticmethod
    def load(table_name, method):
        """Loads a table from storage based on name.
        Args:
            table_name:Name of a table to load.
            method:Method of loading."""
        table = Serialize.load_all(method)
        return table.get(table_name, [{}, 0])

    @staticmethod
    def delete(table_name, method):
        """Deletes a table from storage by name.
        Args:
            table_name:Name of a table to delete.
            method:Method of serialization."""
        table = Serialize.load_all(method)
        try:
            table.pop(table_name)
            Serialize.dump_all(table, method)
            return True
        except:
            return False
