import inspect
import traceback
import readline


class CliControl(object):
    CMDS = ["exit"]

    def __init__(self, pormpt=">>>>"):
        self.pormpt = pormpt
        self.running = True
        readline.set_completer(self.complete)
        readline.parse_and_bind("tab: complete")

    def complete(self, text, state):
        text = text.strip()
        if text:
            cs = [x for x in self.CMDS if x.startswith(text)]
        else:
            cd = self.CMDS
        if state < len(cs):
            return cs[state]
        else:
            -1

    def run(self):
        while self.running:
            cmdlines = raw_input(self.pormpt).strip().split()
            if not cmdlines:
                continue
            elif cmdlines[0] not in self.CMDS:
                print "No such command: %s" % cmdlines[0]
            else:
                f = getattr(self, cmdlines[0])
                argspec = inspect.getargspec(f)
                maxargs = len(argspec.args)
                if argspec.defaults:
                    minargs = maxargs - len(argspec.defaults)
                else:
                    minargs = maxargs
                if not minargs <= len(cmdlines) <= maxargs:
                    print "Wrong args number for: %s" % cmdlines[0]
                else:
                    try:
                        print f(*cmdlines[1:])
                    except Exception, e:
                        print e
                        print traceback.format_exc()

    def exit(self):
        self.running = False
        return "bye!"


class MathCli(CliControl):
    CMDS = ["add", "after", "double", "exit"]

    def add(self, x, y):
        return int(x)+int(y)

    def after(self, x):
        return int(x)+1

    def double(self, x):
        return int(x)*2


if __name__ == '__main__':
    mc = MathCli()
    mc.run()




        