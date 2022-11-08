import os

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-freertos-kernel")
assert os.path.isdir(FRAMEWORK_DIR)

def load_flags(filename):
    if not filename:
        return []
    file_path = os.path.join(FRAMEWORK_DIR, "variants", board.get(
        "build.variant"), "%s.txt" % filename)
    if not os.path.isfile(file_path):
        print("Warning: could not find file '%s'" % file_path)
        return []
    
    with open (file_path, "r") as fp:
        return [f.strip() for f in fp.readlines() if f.strip()]