import os
import subprocess
import ctypes
import sys
import time
from colorama import init, Fore, Back, Style
init(autoreset=True)

try:
    import speedtest
except ImportError:
    print("[ERROR] speedtest-cli module not found. Please install it using 'pip install speedtest-cli'")
    sys.exit(1)

try:
    Speedtest = speedtest.Speedtest
except AttributeError:
    try:
        Speedtest = speedtest.speedtest.Speedtest
    except AttributeError:
        print("[ERROR] Unable to find Speedtest class. Your speedtest-cli version might be incompatible.")
        sys.exit(1)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print(Fore.RED + "[ERROR] Error #1 (Run as Administrator)")
    sys.exit()

def print_title():
    os.system('title Speed Test Tool by @godsnico v1.0' if os.name == 'nt' else '')
    title = r"""
   _____ _____  ______ ______ _____    _______ ______  _____ _______ 
  / ____|  __ \|  ____|  ____|  __ \  |__   __|  ____|/ ____|__   __|
 | (___ | |__) | |__  | |__  | |  | |    | |  | |__  | (___    | |   
  \___ \|  ___/|  __| |  __| | |  | |    | |  |  __|  \___ \   | |   
  ____) | |    | |____| |____| |__| |    | |  | |____ ____) |  | |   
 |_____/|_|    |______|______|_____/     |_|  |______|_____/   |_|   
    """
    print(Fore.CYAN + title)

def animated_progress(message):
    animation = "|/-\\"
    i = 0
    while True:
        i = (i + 1) % len(animation)
        sys.stdout.write(f"\r{Fore.YELLOW}[{animation[i]}] {message}")
        sys.stdout.flush()
        time.sleep(0.1)
        yield

def clear_line():
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()

def speed_test():
    st = Speedtest()
    
    progress = animated_progress("Searching for server")
    for _ in progress:
        try:
            st.get_best_server()
            break
        except:
            pass
    clear_line()
    print(Fore.GREEN + "[+] Server found!")
    
    progress = animated_progress("Testing download speed...")
    for _ in progress:
        try:
            download_speed = st.download() / 1_000_000
            break
        except:
            pass
    clear_line()
    print(Fore.GREEN + f"[+] Download speed Calculated!")
    
    progress = animated_progress("Testing upload speed...")
    for _ in progress:
        try:
            upload_speed = st.upload() / 1_000_000
            break
        except:
            pass
    clear_line()
    print(Fore.GREEN + f"[+] Upload speed Calculated!")
    
    progress = animated_progress("Calculating PING...")
    for _ in progress:
        try:
            ping = st.results.ping
            break
        except:
            pass
    clear_line()
    print(Fore.GREEN + f"[+] PING Calculated!")

    server = st.get_best_server()
    
    
    return download_speed, upload_speed, ping, server

def main():
    print_title()
    download_speed, upload_speed, ping, server = speed_test()

    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(Fore.GREEN + "\n[!] Final Results:")
    print(Fore.WHITE + f"[-] Download Speed: {download_speed:.2f} Mbps")
    print(Fore.WHITE + f"[-] Upload Speed: {upload_speed:.2f} Mbps")
    print(Fore.WHITE + f"[-] Ping: {ping:.2f} ms")
    print(Fore.WHITE + f"[-] Server: {server['sponsor']} in {server['name']}, {server['country']}")
    
    print(Fore.CYAN + "\n[!] Speed test completed. Exiting the program in 20 Seconds...")
    time.sleep(20)
    sys.exit()

if __name__ == "__main__":
    main()