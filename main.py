import random
import sys
import traceback
from colorama import Fore, Back
sys.setrecursionlimit(11000)
import ctypes
import multiprocessing
import os
import secrets
import sys
import threading
import time
from colr import colr
from funcaptcha import ArkoseSession

files = ['raw_created.txt', 'linked.txt', 'purchased.txt']
current_wave = None
current_type = None
start_time = time.time()
solved = 0
failed = 0

def title():
    while True:
        _title_ = f"DortCap | CW: {current_wave} | CV: {current_type}" \
                  f" | T: {time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))}"
        ctypes.windll.kernel32.SetConsoleTitleW(_title_) if os.name == 'nt' else print(f'\33]0;{_title_}\a', end='',
                                                                                       flush=True)
        time.sleep(1)


def test_solve():
    global current_wave, current_type, solved, failed
    while True:
        try:
            _l_ = time.time()
            _l_ -= _l_ % 300
            _l_ = round(_l_)
            data = ArkoseSession(
                "https://iframe.arkoselabs.com",
                random.choice([
                    # "B5B07C8C-F93F-44A8-A353-4A47B8AD5238",
                    "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
                    # "EA4B65CB-594A-438E-B4B5-D0DBA28C9334",
                    # "DF58DD3B-DFCC-4502-91FA-EDC0DC385CFF",
                    # "2F4F0B28-BC94-4271-8AD7-A51662E3C91C",
                    # "73BEC076-3E53-30F5-B1EB-84F494D43DBA",
                    # "3117BF26-4762-4F5A-8ED9-A85E69209A46",
                    # "69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
                    # "A5A70501-FCDE-4065-AF18-D9FAF06EF479"
                ]),
                "https://client-api.arkoselabs.com",
                "https://signup.live.com", {
                    "blob": secrets.token_urlsafe(32)
                },
                "http://wfipdEyz:sdIeqcCssvapoLVI@delta.proxies.cx:47212",
                True
            ).solve(False, False)
            current_wave = data.get('waves')
            current_type = data.get('variant')
            token = data.get("token")
            if data.get('solved'):
                solved +=1
                current_solved = solved
                current_failed = failed
                current_time = time.strftime("%H:%M:%S", time.localtime())
                print(f"{Fore.BLUE}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.BLUE}]{Fore.RESET} {Back.GREEN}Solved{Back.RESET} {Fore.LIGHTBLUE_EX}{current_type}{Fore.RESET} {Fore.LIGHTMAGENTA_EX}{token.split('|')[0]} {Fore.RESET}{current_solved}/{current_failed} Solved: {data.get('solved')} Waves: {data.get('waves')}")
            else:
                failed +=1
               # current_solved = solved
               # current_failed = failed
                #current_time = time.strftime("%H:%M:%S", time.localtime())
               # print(f"{Fore.BLUE}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.BLUE}]{Fore.RESET} {Back.RED}Failed{Back.RESET} {Fore.LIGHTBLUE_EX}{current_type}{Fore.RESET} {Fore.LIGHTMAGENTA_EX}{token.split('|')[0]} {Fore.RESET}{current_solved}/{current_failed} Solved: {data.get('solved')}")
                
        except Exception as e:
            print(e)
            pass


def get_max_threads() -> tuple[int, int]:
    try:
        max_t, max_p = input("Enter (thread/process) count (example: 10/20): ").split("/")
        max_p = int(max_p)
        max_t = int(max_t)
    except Exception:
        print("Not a valid input...")
        return get_max_threads()
    else:
        return max_t, max_p


def main(threads):
    for _ in range(threads):
        threading.Thread(target=test_solve).start()


if __name__ == '__main__':
    os.system("clear" if os.name == "posix" else "cls")
    max_threads, max_processes = get_max_threads()
    threading.Thread(target=title).start()
    main(max_threads)
    for i in range(max_processes):
        multiprocessing.Process(target=main, args=(max_threads,)).start()
        time.sleep(0.5)  # fixes python 3.11 tls client retardation (why?)
