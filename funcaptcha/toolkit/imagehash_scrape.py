import multiprocessing
import random
import sys
import threading
import time
import traceback
from uuid import uuid4
from torch.multiprocessing import Pipe
import httpx
import numpy as np
from torch import multiprocessing

from ..sessions import ArkoseSession

nostealbro = "http://erol:pbwyny3dh@136.175.192.255:65037"
solve_cnt = 0
solve_failed = 0
solve_all = 0
webhook = "https://discord.com/api/webhooks/1123838857247457311/Fd8WunfxC7vybFhPcwVKzgG0FjGCgX8zok6J1LJWMu2L-O-yiZcUiqFgX6Wn6Fh9AbbX"
session_id = uuid4()
encountered_types = []


def cfp_hash(string_in: str) -> int:
    int1 = np.int32(0)
    for int2 in range(len(string_in)):
        int3 = np.int32(ord(string_in[int2]))
        int1 = np.int32((int1 << 5) - int1 + int3)
        int1 = np.bitwise_and(int1, np.int32(-1))
    return int1.item()


def post_fn():
    while True:
        try:
            if solve_cnt > 0:
                httpx.post(webhook, json={
                    "content": f"(Dort) Session ID: {session_id} | Solves: {solve_cnt} | Failed: {solve_failed} | Rate: {int(solve_cnt / solve_all * 100000) / 1000}%\n"
                               f"Encountered Game Types: [{', '.join(encountered_types)}]"
                })
                time.sleep(10)
        except Exception:
            pass


def thread_fn(c_iter: list, send):
    global solve_cnt, solve_failed
    while True:
        try:
            site_key = random.choice(c_iter)
            ases = ArkoseSession("https://iframe.arkoselabs.com",
                                 site_key,
                                 "https://client-api.arkoselabs.com", "outlook", {},
                                 nostealbro).solve(force_gt3=False, audio=True)
            send.send({
                "event_type": "CHALLENGE_ATTEMPT",
                "data": {
                    "site_key": site_key,
                    **ases
                },
                "attempt_id": str(uuid4())
            })
        except Exception:
            pass


def process(c_iter, send):
    for _ in range(25):
        threading.Thread(target=thread_fn, args=(c_iter, send)).start()


def program(fails, solves):
    try:
        global solve_cnt, solve_failed, solve_all
        c_iter = [
            "B5B07C8C-F93F-44A8-A353-4A47B8AD5238",
            # "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
            "EA4B65CB-594A-438E-B4B5-D0DBA28C9334",
            "DF58DD3B-DFCC-4502-91FA-EDC0DC385CFF",
            "2F4F0B28-BC94-4271-8AD7-A51662E3C91C",
            "73BEC076-3E53-30F5-B1EB-84F494D43DBA",
            "3117BF26-4762-4F5A-8ED9-A85E69209A46",
            "69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
            "A5A70501-FCDE-4065-AF18-D9FAF06EF479"
        ]
        # multiprocessing.set_start_method('spawn')
        threading.Thread(target=post_fn).start()
        conn1, conn2 = Pipe(duplex=True)
        for i in range(3):
            multiprocessing.Process(target=process, args=(c_iter, conn2)).start()
        while True:
            data = conn1.recv()
            if isinstance(data, dict):
                if data['event_type'] == 'CHALLENGE_ATTEMPT':
                    attempt_data = data['data']
                    output = solves if attempt_data['game[Solved]'] else fails
                    output.write(f"TK: {attempt_data['game[Token]'].split('|')[0]} | "
                                 f"V: {attempt_data['game[Variant]']} | "
                                 f"W: {attempt_data['game[Waves]']} | "
                                 f"T: {attempt_data['game[Type]']}")
                    if attempt_data['game[Variant]'] not in encountered_types:
                        encountered_types.append(attempt_data['game[Variant]'])
                    solve_all += 1
                    if attempt_data['game[Solved]']:
                        solve_cnt += 1
                    else:
                        solve_failed += 1
    except Exception:
        traceback.print_exc()
