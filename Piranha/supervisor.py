import psutil
from subprocess import PIPE
import gevent
import collections
from Thinkpol import Telescreen

class Worker(Telescreen):
    monitoring = ["pid"]

    def __init__(self, cmd, miniture_addr):
        super(Worker, self).__init__()
        self._connect(miniture_addr)
        self.cmd = cmd
        self.start()

    def start(self):
        self._keeplet = gevent.spawn(self.keep_alive)

    def keep_alive(self):
        self._p = psutil.Popen(self.cmd, shell=False, stdout=PIPE)
        while True:
            if self._p.status != psutil.STATUS_RUNNING:
                self._p = psutil.Popen(self.cmd, shell=False, stdout=PIPE)
            gevent.sleep(1)

    def restart(self):
        self._p.kill()
        self._p = psutil.Popen(self.cmd, shell=False, stdout=PIPE)

    def stop(self):
        self._keeplet.kill(block=True)
        self._p.kill()
        self._close_connection()

    def __getattr__(self, name):
        return getattr(self._p, name)


class Supervisor(object):
    def __init__(self, cmd, miniture_addr):
        self.cmd = cmd
        self.workers = []
        self.miniture_addr = miniture_addr

    def add(self, num):
        for _ in xrange(num):
            self.workers.append(Worker(self.cmd, self.miniture_addr))

    def reduce(self, num):
        for w in self.workers[0:num]:
            w.stop()
        self.workers = self.workers[num:]

    def restart(self, pids=None):
        map(Worker.restart, filter(lambda x: not pids or x.pid in pids, self.workers))
    
    def stop(self, pids):
        stoped = filter(lambda x: not pids or x.pid in pids, self.workers)
        map(Worker.stop, stoped)
        for w in stoped:
            self.workers.remove(w)
