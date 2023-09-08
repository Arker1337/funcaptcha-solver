import base64
import ctypes
import itertools
import json
import multiprocessing
import os
import random
import secrets
import sys
import threading
import time
import traceback

import httpx
from colr import colr

import modded_httpx
from funcaptcha import ArkoseSession

files = ["raw_created.txt", "linked.txt", "purchased.txt"]
current_wave = None
current_type = None
start_time = time.time()
xdd = open("proxies.txt", "r").read().splitlines()
random.shuffle(xdd)
xd = itertools.cycle(xdd)
oxd = len(open("accounts.txt", "r+").read().splitlines())


def title():
    while True:
        xd = len(open("accounts.txt").read().splitlines())
        _title_ = (
            f"DortCap | Created: {xd - oxd} | CW: {current_wave} | CV: {current_type}"
            f" | T: {time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))}"
        )
        ctypes.windll.kernel32.SetConsoleTitleW(_title_) if os.name == "nt" else print(
            f"\33]0;{_title_}\a", end="", flush=True
        )
        time.sleep(1)


def train_rblx():
    global current_wave, current_type
    while True:
        p = next(xd)
        try:
            xd1 = p.split(":")
            p = f"{xd1[2]}:{xd1[3]}@{xd1[0]}:{xd1[1]}"
            print(p)
        except Exception:
            pass
        proxy = "socks5://" + p
        httpc = modded_httpx.Client(proxies=proxy, timeout=10)
        username = secrets.token_hex(4)
        password = secrets.token_urlsafe(6)
        resp = httpc.post(
            "https://auth.roblox.com/v2/signup",
            json={
                "username": username,
                "password": password,
                "birthday": "2003-01-10T05:00:00.000Z",
                "gender": 1,
                "isTosAgreementBoxChecked": True,
                "agreementIds": [
                    "adf95b84-cd26-4a2e-9960-68183ebd6393",
                    "91b2d276-92ca-485f-b50d-c3952804cfd6",
                ],
            },
        )
        login_cs = resp.headers.get("x-csrf-token")
        resp = httpc.post(
            "https://auth.roblox.com/v2/signup",
            headers={"X-Csrf-Token": login_cs},
            json={
                "username": username,
                "password": password,
                "birthday": "2003-01-10T05:00:00.000Z",
                "gender": 1,
                "isTosAgreementBoxChecked": True,
                "agreementIds": [
                    "adf95b84-cd26-4a2e-9960-68183ebd6393",
                    "91b2d276-92ca-485f-b50d-c3952804cfd6",
                ],
            },
        )
        tokens = json.loads(
            base64.b64decode(resp.headers.get("rblx-challenge-metadata").encode())
        )
        dx_blob = tokens.get("dataExchangeBlob")
        c_id = tokens.get("unifiedCaptchaId")
        c_id_r = resp.headers.get("rblx-challenge-id")
        t = time.time()
        data = ArkoseSession(
            "https://www.roblox.com",
            "A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F",
            "https://roblox-api.arkoselabs.com",
            "roblox_register",
            {"blob": dx_blob},
            "http://1Month1:product--resi6--pass--Proxies@resi.ipv6.plainproxies.com:8080",
            True,
        ).solve()
        current_wave = data.get("waves")
        current_type = data.get("variant")
        token = data.get("token")
        nt = time.time()
        if data.get("solved"):
            current_time = time.strftime("%H:%M:%S", time.localtime())
            sys.stdout.write(
                f"[{colr.Colr().hex('#525052', current_time)}] {colr.Colr().hex('#fc0335', 'Roblox FunCaptcha')} "
                f"{colr.Colr().hex('#adaaad', 'Solved')} "
                f"{colr.Colr().hex('#8093f1', token.split('|')[0])} ({round(nt - t, 2)}s)\n"
            )
            sys.stdout.flush()
            jsd = {
                "unifiedCaptchaId": c_id,
                "captchaToken": token,
                "actionType": "Signup",
            }
            resp = httpc.post(
                "https://auth.roblox.com/v2/signup",
                headers={
                    "X-Csrf-Token": login_cs,
                    "Rblx-Challenge-Id": c_id_r,
                    "rblx-challenge-type": "captcha",
                    "Rblx-Challenge-Metadata": base64.b64encode(
                        json.dumps(jsd).encode()
                    ).decode(),
                },
                json={
                    "username": username,
                    "password": password,
                    "birthday": "2003-01-10T05:00:00.000Z",
                    "gender": 3,
                    "isTosAgreementBoxChecked": True,
                    "agreementIds": [
                        "adf95b84-cd26-4a2e-9960-68183ebd6393",
                        "91b2d276-92ca-485f-b50d-c3952804cfd6",
                    ],
                },
            )
            if resp.json().get("userId"):
                current_time = time.strftime("%H:%M:%S", time.localtime())
                sys.stdout.write(
                    f"[{colr.Colr().hex('#525052', current_time)}] {colr.Colr().hex('#fc0335', 'Roblox Register')} "
                    f"{colr.Colr().hex('#adaaad', 'Created')} "
                    f"{colr.Colr().hex('#8093f1', f'{username}:{password}')}\n"
                )
                sys.stdout.flush()
                with open("accounts.txt", "a+") as fp:
                    fp.write(f"{username}:{password}\n")
                    fp.close()
                with open("cookies.txt", "a+") as fp:
                    fp.write(f".ROBLOSECURITY={resp.cookies.get('.ROBLOSECURITY')}\n")
                    fp.close()
            pass


def test_solve():
    while True:
        try:
            train_rblx()
        except Exception:
            pass


def get_max_threads() -> tuple[int, int]:
    try:
        max_t, max_p = input("Enter (thread/process) count (example: 10/20): ").split(
            "/"
        )
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


if __name__ == "__main__":
    os.system("clear" if os.name == "posix" else "cls")
    max_threads, max_processes = get_max_threads()
    threading.Thread(target=title).start()
    main(max_threads)
    for i in range(max_processes):
        multiprocessing.Process(target=main, args=(max_threads,)).start()
        time.sleep(0.5)  # fixes python 3.11 tls client retardation (why?)
