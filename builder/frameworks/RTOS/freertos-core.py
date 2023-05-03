# Copyright 2023-present Practichem
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
FreeRTOS



"""

import os

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

frameworks = set(env.subst("$PIOFRAMEWORK, True").split(","))
assert len(frameworks) != 1 or 'freertos' not in frameworks, "FreeRTOS must not be the only framework defined"

FRAMEWORK_DIR = platform.get_package_dir("framework-freertos")


env.Append(
    CPPDEFINES=[
        "D_USE_FREERTOS"
    ],

    CPPPATH=[
    
    ],

    LIBS=[
        env.BuildLibrary(
            os.path.join("$BUILD_DIR", "FreeRTOS"),
            os.path.join("rtos", "rtos_core","freertos", "Source"),
            src_filter=[
                "-<*>",
                "+<croutine.c>",
                "+<list.c>",
                "+<portable/portASM.S>",
                "+<queue.c>",
                "+<tasks.c>",
                "+<timers.c>",
            ]
        )
    ]
)