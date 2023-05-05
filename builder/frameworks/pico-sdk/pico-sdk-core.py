# 2023 Collin Brown
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import print_function
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()

env.framework_dir = env.PioPlatform().get_package_dir("framework-pico-sdk")
env.libs = []



