import os

from SCons.Script import DefaultEnvironment, SConscript


env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-freertos-kernel")
assert os.path.isdir(FRAMEWORK_DIR)

env.Export('env')
SConscript(os.path.join(FRAMEWORK_DIR, "lib_build.py"), 'env')

#KERNEL_PATH = os.path.join(FRAMEWORK_DIR,"FreeRTOS-Kernel")

#CPPPATH = [
#    os.path.join(FRAMEWORK_DIR, "FreeRTOS-Kernel", "include"),
#    os.path.join(FRAMEWORK_DIR, "FreeRTOS-Kernel", "portable","GCC","ARM_CM0"),
#    os.path.join(FRAMEWORK_DIR, "variants", board.get("build.variant")),
#]

#libs = []

#if "build.variant" in board:
#    env.Append(CPPPATH=CPPPATH)

#libs.append(
#    env.BuildLibrary(
#        os.path.join("$BUILD_DIR", "FrameworkFreeRTOSKernel"),
#        os.path.join(FRAMEWORK_DIR),
#        [
#            "+<FreeRTOS-Kernel/>",
#            "-<FreeRTOS-Kernel/portable/>",
#            "+<FreeRTOS-Kernel/portable/MemMang/heap_3.c>"
#            "+<FreeRTOS-Kernel/portable/GCC/ARM_CM0/>"
#        ]
#    )
#)

#env.Prepend(LIBS=libs)