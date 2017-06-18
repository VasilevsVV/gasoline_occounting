import pickle as p
import os


class Serialize:
    pickle = 1
    yaml = 2
    json = 3

    @staticmethod
    def dump(table_name, data, method):
        if method == Serialize.pickle:
            with open(dict(os.environb)[b'HOME'] + b'/.gas_storage.pickle', 'wb+') as f:
                try:
                    table = p.load(f)
                except:
                    table = {}
                table[table_name] = data
                p.dump(table, f)
                f.close()

    @staticmethod
    def load(table_name, method):
        if method == Serialize.pickle:
            with open(dict(os.environb)[b'HOME'] + b'/.gas_storage.pickle', 'wb+') as f:
                try:
                    table = p.load(f)
                except:
                    table = {}
            return table.get(table_name, [{}, 0])

    @staticmethod
    def delete(table_name, method):
        if method == Serialize.pickle:
            with open(dict(os.environb)[b'HOME'] + b'/.gas_storage.pickle', 'wb+') as f:
                try:
                    table = p.load(f)
                    if table.get(table_name, False):
                        table.pop(table_name)
                        p.dump(table, f)
                        return True
                    else:
                        return False
                except:
                    return False
