import os
import ujson as json
import tabulate


class Writer:
    def add(self, metrics):
        raise NotImplementedError()


class ConsoleWriter(Writer):

    def __init__(self):
        self.header = set()
        self.cache = []

    def add(self, metrics):
        for k in metrics.keys():
            self.header.add(k)
        self.cache.append(metrics)
        header = sorted(list(self.header))
        rows = []
        for m in self.cache:
            rows.append([m.get(k, None) for k in header])
        s = tabulate.tabulate(rows, headers=header)
        s = "\033[F" * (len(s.splitlines()) - 1) + s
        print(s)


class FileWriter(Writer):

    def __init__(self, fname):
        self.fname = fname
        if os.path.isfile(fname):
            os.remove(fname)

    def add(self, metrics):
        with open(self.fname, 'a') as f:
            f.write('{}\n'.format(json.dumps(metrics)))
            f.flush()



if __name__ == '__main__':
    w = FileWriter('my_exp')
    import time
    for i in range(10):
        print(i)
        w.add({'iteration': i, 'score': i+1})
        time.sleep(1)
