import signal
import threading
import curio
import subprocess
import ctypes, os, sys, shutil
import urllib.request
import win32pipe
import winreg
import time
import yaml
starttime = time.time()

created_process = list()
f = curio.TaskGroup()

a = 1

PROCESSES = (
    "fakeprocess1.exe",
    "fakeprocess2.exe",
)






def init_colors():
    kernel32 = ctypes.WinDLL("kernel32")
    hStdOut = kernel32.GetStdHandle(-11)
    mode = ctypes.c_ulong()
    kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
    mode.value |= 4
    kernel32.SetConsoleMode(hStdOut, mode)


def print_log(log):
    print("\033[92m [OK] \x1b[0m", log)




def start_fake_process(path, process_name):
    print_log(f"Starting fake process : {process_name}")
    shutil.copyfile(f"{path}\\fake.exe", f"{path}\\{process_name}")
    proc = subprocess.Popen(
        path + "\\" + process_name,
        shell=False,
        stdin=None,
        stdout=None,
        stderr=None,
        close_fds=True,
        creationflags=0x00000008,  # DETACHED_PROCESS
    )
    return proc




def create_process(path):
#    with open('p.yaml') as f:
#	    my_dict = yaml.safe_load(f)
#
#    txt = my_dict["PROCESSES"]
#    print_log(txt)


    return [start_fake_process(path, process_name) for process_name in PROCESSES]



async def setup_sc(path, created_process):
    init_colors()
    created_process.extend(create_process(path))


def signal_handler(sig, frame):
    for proc in created_process:
        proc.kill()
    print_log("FINISHED")
    os._exit(0)



def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())

def heartbeat(i):
    print_log("tick")
        
    if process_exists(i):
        print_log(f"{i} is running, sir.")
    else:
        print_log(f"{i} is running..... not.")
        webUrl  = urllib.request.urlopen("CANARY_TOKEN_URL")
    time.sleep(1.0 - ((time.time() - starttime) % 1.0))	

async def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)
    if ctypes.windll.shell32.IsUserAnAdmin():
        await f.spawn(setup_sc,os.path.dirname(sys.argv[0]),created_process)
    while(True):
        await curio.sleep(1)
        print_log("loop")

        for i in PROCESSES:
        	heartbeat(i)
        #return [heartbeat(process_name) for process_name in PROCESSES]

if __name__ == "__main__":
    curio.run(main)
