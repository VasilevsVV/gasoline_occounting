import pickle as p


class Serialize:
    def dump(table_name, data, method):
        if method == "pickle":
            with open('~/.gas_storage', 'wb+') as f:
                try:
                    table = p.load(f)
                except:
                    table = {}
                table[table_name] = data
                p.dump(table, f)
                f.close()

    def load(table_name, method):
        if method == "pickle":
            with open('~/.gas_storage', 'wb+') as f:
                try:
                    table = p.load(f)
                except:
                    table = {}
            return table.get(table_name, [{}, 0])
