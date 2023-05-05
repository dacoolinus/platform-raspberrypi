from sys import platform
import subprocess
from re import split as re_split
from re import search as re_search
from platform import system # pyright: reportShadowedImports=false
from os.path import join, isdir, isfile
from os import environ, listdir
from time import sleep
from serial import Serial

from frameworks._common import do_write

INFO_FILE_NAME = "/INFO_UF2.TXT"

def board_id(path):
    with open(path + INFO_FILE_NAME, "r") as f:
        file_content = f.read()
    return re_search("Board-ID: ([^\r\n]*)", file_content).group(1)

def get_drives():
    drives = []
    if platform == 'win32':
        r = subprocess.check_output(["wmic", "PATH", "Win32_LogicalDisk", "get", "DeviceID,", "VolumeName,", "FileSystem,", "DriveType"])
        for line in (r.decode('utf-8')).split('\n'):
            words = re_split('\s+', line)
            if len(words) >= 3 and words[1] == "2" and words[2] == "FAT":
                drives.append(words[0])
    else:
        rootpath = "/media"
        if platform == "darwin":
            rootpath = "/Volumes"
        elif platform == "linux":
            tmp = rootpath + "/"  + environ["USER"]
            if isdir(tmp):
                rootpath = tmp
        for d in listdir(rootpath):
            drives.append(join(rootpath, d))

    def has_info(d):
        try:
            return isfile(d + INFO_FILE_NAME)
        except:
            return False
    return list(filter(lambda d: isfile(d + INFO_FILE_NAME), drives))

def uploader(target, source, env):
    global appstartaddr
    appstartaddr = int(env.address, 0)
    bin_name = join(env.get("BUILD_DIR"), env.get("PROGNAME")) + ".bin"
    uf2_name = join(env.get("BUILD_DIR"), env.get("PROGNAME")) + ".uf2"
    drive = env.get("UPLOAD_PORT")
    if env.GetProjectOption("monitor_port") != None:
        try: 
            usb = Serial(env.GetProjectOption("monitor_port"), 1200)
            sleep(1)
            usb.close()
        except:
            pass
        sleep(1)
        if 'windows' not in system(): sleep(1)
    with open(bin_name, mode='rb') as f: inpbuf = f.read()
    outbuf = convert_to_uf2(inpbuf)
    sleep(1)
    do_write(uf2_name, outbuf)
    drives = get_drives()
    if len(drives) == 0:
        print("No drives found")
        return
    for d in drives:
        print("Flashing %s (%s)" % (d, board_id(d)))
        do_write(d +'/'+ env.get("PROGNAME")+'.uf2', outbuf) # write ufs to pico
    sleep(1) # usb-serial driver up