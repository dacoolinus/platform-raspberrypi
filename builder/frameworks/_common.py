from distutils.log import error
import os
from os.path import join
from shutil import copy2
from colorama import Fore
from SCons.Script import Builder

binary_type_info  = []

def do_copy(src, dst, name):
    file_name = os.path.join(dst, name)
    return file_name if os.path.exists(file_name) else copy2(os.path.join(src, name), file_name)

def do_mkdir(path, name):
    dir = os.path.join(path, name)
    return dir if os.path.isdir(dir) else os.makedirs(dir, exist_ok=True) or dir

def do_write(name, buf):
    with open(name, "wb") as f:
        f.write(buf)

def do_create_freertos_template(env):
    src = join(env.PioPlatform.get_package_dir('framework-freertos'), 'templates')

def do_create_VFS_template(env):
    src = join(env.PioPlatform.get_package_dir('package-vfs'), 'templates')
