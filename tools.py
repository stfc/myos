import subprocess

class Results(object):
    def __init__(self, cmd, out, err, rc):
        self.cmd = cmd
        self.out = out
        self.err = err
        self.rc = rc


def run(cmd):
    subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    (out, err) = subproc.communicate()
    st = subproc.returncode
    results = Results(cmd, out.strip(), err.strip(), st)
    return results
