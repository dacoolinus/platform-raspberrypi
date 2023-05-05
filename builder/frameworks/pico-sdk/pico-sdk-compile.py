from os.path import join
from SCons.Script import Builder

def pico_sdk_compiler(env, application_name='APPLICATION'):
    env["FRAMEWORK_DIR"] = env.framework_dir
    env.sdk = env.BoardConfig().get("build.sdk", "SDK") # get/set default SDK
    env.variant = env.BoardConfig().get("build.variant", "raspberry-pi-pico")
    env.wifi = env.BoardConfig().get("build.wifi", False)

    env.Replace(
        BUILD_DIR = env.subst("$BUILD_DIR").replace("\\", "/"),
        AR="arm-none-eabi-ar",
        AS="arm-none-eabi-as",
        CC="arm-none-eabi-gcc",
        GDB="arm-none-eabi-gdb",
        CXX="arm-none-eabi-g++",
        OBJCOPY="arm-none-eabi-objcopy",
        RANLIB="arm-none-eabi-ranlib",
        SIZETOOL="arm-none-eabi-size",
        ARFLAGS=["rc"],
        SIZEPROGREGEXP=r"^(?:\.text|\.data|\.boot2|\.rodata)\s+(\d+).*",
        SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.ram_vector_table)\s+(\d+).*",
        SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
        SIZEPRINTCMD='$SIZETOOL --mcu=$BOARD_MCU -C -d $SOURCES',
        PROGSUFFIX=".elf",
        PROGNAME = application_name
    )

    cortex = ["-march=armv6-m", "-mcpu=cortex-m0plus", "-mthumb"]
    env.heap_size = env.BoardConfig().get("build.heap", "2048")
    optimization = env.BoardConfig().get("build.optimization", "-Os")
    stack_size = env.BoardConfig().get("build.stack_size", "2048")

    env.Append(
        ASFLAGS=[ cortex, "-x", "assembler-with-cpp" ],
        CPPPATH=[
            join("$PROJECT_DIR", "src"),
            join("$PROJECT_DIR", "lib"),
            join("$PROJECT_DIR", "include"),
        ],
        CPPDEFINES=[
            "NDEBUG",
            "PICO_ON_DEVICE=1",
            "PICO_HEAP_SIZE=" + env.heap_size,
            "PICO_STACK_SIZE=" + stack_size,
        ],
        CCFLAGS=[
            cortex,
            optimization,
            "-fdata-sections",
            "-ffunction-sections",
            "-Wall",
            "-Wextra",
            "-Wfatal-errors",
            "-Wno-sign-compare",
            "-Wno-type-limits",
            "-Wno-unused-parameter",
            "-Wno-unused-function",
            "-Wno-unused-but-set-variable",
            "-Wno-unused-variable",
            "-Wno-unused-value",
            "-Wno-strict-aliasing",
            "-Wno-maybe-uninitialized"
        ],
        CFLAGS=[
            cortex,
            "-Wno-discarded-qualifiers",
            "-Wno-ignored-qualifiers",
            "-Wno-attributes"
        ],
        CXXFLAGS=[
            "-fno-rtti",
            "-fno-exceptions",
            "-fno-threadsafe-statics",
            "-fno-non-call-exceptions",
            "-fno-use-cxa-atexit",
        ],
        LINKFLAGS=[
            cortex,
            optimization,
            "-nostartfiles",
            "-Xlinker", "--gc-sections",
            "-Wl", "--gc-sections",
            "--entry=_entry_point",
            dev_nano(env)
        ],
        LIBSOURCE_DIRS = [ join(env.framework_dir, "library"), ],
        LIBPATH = [ join(env.framework_dir, "library"), join("$PROJECT_DIR", "lib") ],
        LIBS = ['m', 'gcc'],
        BUILDERS = dict( 
            ElfToBin = Builder(
                action = env.VerboseAction(" ".join([
                    "$OBJCOPY", "-O", "binary",
                    "$SOURCES", "$TARGET",
                ]), "Building $TARGET"),
                suffix = ".bin"
        ),
        UPLOADCMD = dev_uploader
    )
    if False == env.wifi:                       #type: ignore
        env.Append(CPPDEFINES = ["PICO_WIFI"])