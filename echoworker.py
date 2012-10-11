from Piranha import BaseWorker, config
from time import sleep

class EchoWorker(BaseWorker):
    def handle(self, msg):
        print msg
        print "starting"
        sleep(1)
        print "ending"
        return msg, None

if __name__ == '__main__':
    EchoWorker().run((config.queuepool_host, config.queuepool_port), "echo")
