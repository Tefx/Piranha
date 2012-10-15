from Piranha import MultiTaskWorker, config
from redis import StrictRedis
import Husky

class UncertaintyWorker(MultiTaskWorker):
    def __init__(self, db_conf):
        super(UncertaintyWorker, self).__init__()
        self.redis = StrictRedis(host=db_conf["host"], port=db_conf["port"], db=db_conf["db"])

    def reg_mod(self, name, mod):
        self.redis.set("mod_%s" % name, Husky.dumps(mod))

    def calculate(self, formula):
        pass

if __name__ == '__main__':
    UncertaintyWorker({"host":"localhost", "port":6379, "db":1}).run((config.queuepool_host, config.queuepool_port), "Uncertainty")
        