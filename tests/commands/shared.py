import os.path
import sys


def get_test_app():
    docker_sample = "/home/weppy/sample_app.py"
    if os.path.isfile(docker_sample):
        return docker_sample
    return os.path.join(os.path.dirname(__file__), "sample_app.py")

TEST_APP = get_test_app()

def get_prog():
    """Check whether weppyn is installed in virtualenv and return path
    to proper executable."""
    if os.path.isfile(os.path.join(sys.prefix, "bin/weppyn")):
        return os.path.join(sys.prefix, "bin/weppyn")
    return os.path.join(sys.prefix, "Scripts/weppyn")


PROG = get_prog()
