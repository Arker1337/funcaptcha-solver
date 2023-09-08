import json
from io import BytesIO
from typing import Union, IO
import modded_httpx as httpx


def _replace_resp(resp: str):
    # most of these were made by me, others belong to "useragents" on GitHub.
    resp = resp.lower()
    replacements = {
        "weinstein": "17",
        "/": "",
        "the": "0",
        "please": "3",
        "brie": "3",
        "river": "0",
        "sex": "6",
        "tube": "2",
        "over": "4",
        "liver": "0",
        "europe": "0",
        "play": "5",
        "text": "6",
        "book": "6",
        "vibe": "5",
        "thor": "4",
        "hai": "5",
        "one": "1",
        "to": "2",
        "two": "2",
        "tree": "3",
        "three": "3",
        "four": "4",
        "jeden": "7",
        "for": "4",
        "or": "4",
        "zero": "0",
        "do": "5",
        "right": "5",
        "hero": "4",
        "five": "5",
        "six": "6",
        "nine": "9",
        "white": "1",
        "whine": "1",
        "dial": "69",
        "wine": "1",
        "guys": "9",
        "sides": "9",
        "store": "44",
        "door": "04",
        "side": "9",
        "buy": "55",
        "rightly": "53",
        "rightfully": "53",
        "lee": "53",
        "now": "9",
        "eight": "8",
        "soon": "2",
        "wireless": "8",
        "find": "5",
        "rise": "1",
        "italy": "34",
        "ice": "0",
        "lights": "9",
        "light": "9",
        "sites": "9",
        "pwell": "9",
        "well": "9",
        "size": "9",
        "by": "1",
        "knights": "9",
        "knight": "9",
        "nights": "9",
        "night": "9",
        "-": "",
        " ": "",
        "r": "9",
        "l": "2",
        "a": "4"
    }
    for key in replacements:
        if key in resp:
            resp = resp.replace(key, replacements[key])
    return resp


def solve_old(audio: bytes) -> str:
    request = httpx.post(
        "http://www.google.com/speech-api/v2/recognize?client=chromium&lang=en&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw",
        content=audio, headers={"Content-Type": "audio/l16; rate=%s" % 8000}, timeout=500)
    answer: Union[str, None] = None
    actual_result = json.loads(request.text.split('\n')[1]).get("result")[0]
    if "alternative" in actual_result:
        for prediction in actual_result["alternative"]:
            if "transcript" in prediction:
                answer = prediction["transcript"]
    if answer is None:
        raise LookupError("Speech is unintelligible")
    return _replace_resp(answer)
