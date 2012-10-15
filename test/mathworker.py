from Piranha import MultiTaskWorker, config

class Math(MultiTaskWorker):
    def add(self, x, y):
        return x+y

    def double(self, x):
        return x*2

if __name__ == '__main__':
    Math().run((config.queuepool_host, config.queuepool_port), "math")