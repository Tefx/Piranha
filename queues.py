from Piranha import config
from Corellia import Worker
from Piranha import QueuePool

if __name__ == '__main__':
    Worker(QueuePool, config.queuesconfig).run_alone(config.queuepool_port)