import base64
import json
import random
import sys
import time
import traceback
from typing import Union

from colr import colr

from funcaptcha import fingerprinting
from funcaptcha.algorithms import hash_mp3
from funcaptcha.utilities import nopecha
from funcaptcha.utilities.captcha import audio_helper, breakers
from funcaptcha.utilities.databases import image_database, audio_database
from funcaptcha.utilities.databases.image_database import Grid
from funcaptcha.utilities.encryption import crypt
from modded_httpx import Client


def data_to_dict(data: dict[str, str]) -> dict[str, str]:
    new_dict: dict[str, str] = {}
    for x in data:
        if data[x]:
            new_dict.update({
                f"data[{x}]": data[x]
            })
    return new_dict


class ArkoseSession(Client):

    def __init__(self, site_url: str, site_key: str, arkose_api_url: str,
                 captcha_page_url: str, data: dict[str, Union[str, None]], proxy: Union[str, None],
                 debug: bool = False):
        super().__init__(proxies=proxy, http2=True, timeout=9999)
        self.proxies = proxy
        self.site_url = site_url
        self.site_key = site_key
        self.arkose_api_url = arkose_api_url
        self.captcha_page_url = captcha_page_url
        self.data = data
        self.debug = debug

    def solve(self, audio: bool = False, force_gt3: bool = False, force_chl: bool = False,
              nopecha_key: Union[str, None] = None, custom_user_agent: Union[str, None] = None,
              attempt_force_easy_challenge: bool = True):
        render_type: str = 'noJS' if force_gt3 else "canvas"
        fingerprint_data = fingerprinting.get_fingerprint(self.captcha_page_url, custom_user_agent,
                                                          attempt_force_easy_challenge)
        heads = round(random.random(), 1)
        agent_v = str(random.randint(1, 2114))
        language = fingerprint_data.raw_bda.get('lang-header')
        if not language:
            language = f"en-US,en;q={heads}"
        if 'Chrome/' in fingerprint_data.agent:
            agent_v = fingerprint_data.agent.split("Chrome/")[1].split(".")[0]
        chrome_user_agent_brands = f'"Not.A/Brand";v="{random.randint(1, 2116)}", "Chromium";v="{agent_v}", "Chrome";v="{agent_v}"'
        platform_token = '"Android"' if "Android" in fingerprint_data.agent else '"CriOS"' if 'CriOS' in fingerprint_data.agent else '"Windows"'
        is_mobile = "?1" if 'Android' or 'CriOS' in platform_token else "?0"
        extra_headers = {
            "Sec-Ch-Ua": chrome_user_agent_brands,
            'Sec-Ch-Ua-Platform': platform_token,
            'Sec-Ch-Ua-Mobile': is_mobile
        } if 'Firefox' not in fingerprint_data.agent else {
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-User": "?1"
        }
        self.get(f"https://iframe.arkoselabs.com/{self.site_key}/index.html?mkt=en-US", headers={
            'Accept': '*/*',
            'Accept-Encoding': '*/*',
            'Accept-Language': language,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.arkose_api_url,
            'Referer': f'https://iframe.arkoselabs.com/',
            **extra_headers,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': fingerprint_data.agent
        })
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': '*/*',
            'Accept-Language': language,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.arkose_api_url,
            'Referer': f'{self.arkose_api_url}/v2/1.5.4/enforcement.cd12da708fe6cbe6e068918c38de2ad9.html',
            **extra_headers,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': fingerprint_data.agent
        }
        data = {
            "bda": fingerprint_data.fingerprint,
            "public_key": self.site_key,
            "site": self.site_url,
            "userbrowser": fingerprint_data.agent,
            "capi_version": "1.5.4",
            "capi_mode": "inline",
            "style_theme": "default",
            "rnd": round(random.random(), 14),
            **data_to_dict(self.data)
        }
        self.cookies.set("timestamp", str(int(time.time() * 1000)))
        session_data = self.post(
            f'{self.arkose_api_url}/fc/gt2/public_key/{self.site_key}',
            headers=headers,
            data=data,
        ).json()
        full_token = session_data.get("token")
        session_token = full_token.split("|")[0]
        if not force_chl:
            if 'sup=1' in full_token:
                # print(fingerprint_data.agent)
                return {
                    "waves": 1,
                    "variant": "SILENT_PASS",
                    "type": 0,
                    "solved": True,
                    "token": full_token,
                }
        region = full_token.split("|r=")[1].split("|")[0]
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': '*/*',
            'Accept-Language': language,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.arkose_api_url,
            'Referer': f'{self.arkose_api_url}/fc/assets/ec-game-core/game-core/1.14.1/standard/index.html?session={full_token.replace("|", "&")}',
            **extra_headers,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': fingerprint_data.agent,
        }
        data = {
            'token': session_token,
            'sid': region,
            'render_type': render_type,
            'lang': 'en',
            'isAudioGame': json.dumps(audio),
            'analytics_tier': '40',
            'apiBreakerVersion': 'green',
        }
        challenge = self.post(f'{self.arkose_api_url}/fc/gfct/', headers=headers,
                              data=data).json()
        game_data = challenge["game_data"]
        custom_gui = game_data["customGUI"]
        game_token = challenge["challengeID"]
        game_type = game_data["gameType"]
        ref = challenge.get('challengeURL',
                            f'{self.arkose_api_url}/fc/assets/ec-game-core/game-core/1.14.1/standard/index.html?session={full_token.replace("|", "&")}')
        if game_type != 101:
            images = custom_gui["_challenge_imgs"]
            variant = game_data["game_variant"] if game_type == 3 else game_data["instruction_string"]
            # if len(images) <= 2:
            #     print(fingerprint_data.agent, len(images))
            instructions = challenge["string_table"][f"{game_type}.instructions-{variant}"]
            game_difficulty = game_data.get('game_difficulty')
            api_breakers = custom_gui.get("api_breaker")
            ts = str(round(time.time() / 1000))
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': '*/*',
                'Accept-Language': language,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': self.arkose_api_url,
                'Referer': f'{ref}?session={full_token.replace("|", "&")}',
                **extra_headers,
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': fingerprint_data.agent,
            }
            data = {
                'session_token': session_token,
                'game_token': game_token,
                'sid': region,
            }
            response = self.post(f'{self.arkose_api_url}/fc/ekey/', headers=headers, data=data).json()
            decryption_key = response.get('decryption_key')
            answers: list = []
            answers_found: list = []
            answers_raw: list = []
            found = False
            for x in images:
                image_bytes = self.get(x, headers=headers).content
                try:
                    image_bytes = base64.b64decode(crypt.decrypt(image_bytes, decryption_key))
                except Exception:
                    pass
                hand_hash: Union[str, None]
                grid = Grid(game_difficulty, image_bytes, game_type == 4)
                if game_type == 4:
                    answer, hand_hash, found2 = image_database.get_image_validity_type4(grid, variant, game_difficulty, instructions)
                else:
                    answer, found2 = image_database.get_image_validity_type3(grid, variant, instructions)
                    if nopecha_key and not found2:
                        answer = nopecha.classify(base64.b64encode(image_bytes).decode(), instructions)
                        found = True
                if found2:
                    found = True
                answers.append(breakers.fix_answer(game_type, api_breakers, answer, grid.img.size == (450, 300)))
                answers_raw.append((answer, grid))
                if found:
                    answers_found.append(answer)
                headers: dict = {
                    'accept': '*/*',
                    'Accept-Language': language,
                    'cache-control': 'no-cache',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': self.arkose_api_url,
                    'referer': f'{ref}?session={full_token.replace("|", "&")}',
                    **extra_headers,
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': fingerprint_data.agent,
                    'x-newrelic-timestamp': ts,
                    'x-requested-with': 'XMLHttpRequest',
                }
                data = {
                    'session_token': session_token,
                    'game_token': game_token,
                    'sid': region,
                    'guess': crypt.encrypt(json.dumps(answers, separators=(",", ":")), session_token),
                    "render_type": render_type,
                    'analytics_tier': '40',
                    'bio': "",
                }
                response = self.post(f'{self.arkose_api_url}/fc/ca/', headers=headers,
                                     data=data).json()
                decryption_key = response.get('decryption_key')
                if response.get('solved'):
                    if found and self.debug:
                        current_time = time.strftime("%H:%M:%S", time.localtime())
                        sys.stdout.write(
                            f"[{colr.Colr().hex('#525052', current_time)}] {colr.Colr().hex('#04e762', 'Arkose FunCaptcha')} "
                            f"{colr.Colr().hex('#adaaad', variant.upper())} "
                            f"{colr.Colr().hex('#b388eb', json.dumps(answers_found))}\n")
                        sys.stdout.flush()
                    for xd in answers_raw:
                        if game_type == 4:
                            image_database.save_good_type4(xd[0], variant, xd[1])
                            image_database.save_bad_type4(xd[0], variant, xd[1])
                        else:
                            image_database.save_good_type3(xd[0], variant, xd[1])
                            image_database.save_bad_type3(xd[0], variant, xd[1])
                    return {
                        "waves": len(images),
                        "variant": variant.upper(),
                        "type": game_type,
                        "token": full_token,
                        "solved": True
                    }
                if response.get('solved') is not None:
                    if found and self.debug:
                        current_time = time.strftime("%H:%M:%S", time.localtime())
                        sys.stdout.write(
                            f"[{colr.Colr().hex('#525052', current_time)}] {colr.Colr().hex('#04e762', 'Arkose FunCaptcha')} "
                            f"{colr.Colr().hex('#adaaad', variant.upper())} "
                            f"{colr.Colr().hex('#b388eb', json.dumps(answers_found))}\n")
                        sys.stdout.flush()
                    return {
                        "waves": len(images),
                        "variant": variant.upper(),
                        "type": game_type,
                        "token": full_token,
                        "solved": False
                    }
        else:
            if render_type == 'noJS' or render_type == 'liteJS':
                response = self.get(
                    f"{self.arkose_api_url}/fc/get_audio/?session_token={session_token}&analytics_tier=40&r={region}"
                    f"&game=0&language=en",
                    headers={
                        "accept": '*/*',
                        "accept-encoding": '*/*',
                        "accept-language": language,
                        "cache-control": 'no-cache',
                        "content-type": 'application/x-www-form-urlencoded; charset=UTF-8',
                        "origin": self.arkose_api_url,
                        "referer": f'{self.arkose_api_url}/fc/gc/?token={full_token.replace("&", "|")}',
                        **extra_headers,
                        "sec-fetch-dest": 'empty',
                        "sec-fetch-mode": 'cors',
                        "sec-fetch-site": 'same-origin',
                        "user-agent": fingerprint_data.agent,
                        "x-requested-with": 'XMLHttpRequest',
                    }, follow_redirects=True).content
                if b"DENIED ACCESS" not in response:
                    response = self.post(f"{self.arkose_api_url}/fc/audio/", data={
                        "session_token": session_token,
                        "analytics_tier": "40",
                        "response": audio_helper.solve_old(response),
                        "language": "en",
                        "r": region,
                        "audio_type": "2",
                        "bio": ""
                    }, headers={
                        "accept": '*/*',
                        "accept-encoding": '*/*',
                        "accept-language": language,
                        "cache-control": 'no-cache',
                        "content-type": 'application/x-www-form-urlencoded; charset=UTF-8',
                        "origin": self.arkose_api_url,
                        "referer": f'{self.arkose_api_url}/fc/gc/?token={full_token.replace("&", "|")}',
                        **extra_headers,
                        "sec-fetch-dest": 'empty',
                        "sec-fetch-mode": 'cors',
                        "sec-fetch-site": 'same-origin',
                        "user-agent": fingerprint_data.agent,
                        "x-requested-with": 'XMLHttpRequest',
                    }).json()
                    if response.get('response') == 'correct':
                        return {
                            "waves": 1,
                            "variant": "NUMBER_AUDIO",
                            "type": game_type,
                            "token": full_token,
                            "solved": True
                        }
                else:
                    return {
                        "waves": 1,
                        "variant": "NUMBER_AUDIO",
                        "type": game_type,
                        "token": full_token,
                        "solved": False
                    }
            else:
                audio_urls = challenge['audio_challenge_urls']
                variant = game_data["game_variant"]
                answers = []
                hashes: list[tuple[str, int]] = []
                answers_found: list[int] = []
                answer_found: bool = False
                for i in range(len(audio_urls)):
                    audio_data: bytes = self.get(audio_urls[i], follow_redirects=True, headers={
                        "accept": '*/*',
                        "accept-encoding": '*/*',
                        "accept-language": language,
                        "cache-control": 'no-cache',
                        "content-type": 'application/x-www-form-urlencoded; charset=UTF-8',
                        "origin": self.arkose_api_url,
                        "referer": f'{self.arkose_api_url}/fc/gc/?token={full_token.replace("&", "|")}',
                        **extra_headers,
                        "sec-fetch-dest": 'empty',
                        "sec-fetch-mode": 'cors',
                        "sec-fetch-site": 'same-origin',
                        "user-agent": fingerprint_data.agent,
                        "x-requested-with": 'XMLHttpRequest',
                    }).content
                    audio_hash = hash_mp3(audio_data)
                    answer = audio_database.check_valid_audio(audio_hash, variant)
                    hashes.append((audio_hash, answer[0]))
                    if answer[1]:
                        answers_found.append(answer[0])
                        answer_found = True
                    answers.append(str(answer[0]))
                current_time = time.strftime("%H:%M:%S", time.localtime())
                if answer_found and self.debug:
                    sys.stdout.write(
                        f"[{colr.Colr().hex('#525052', current_time)}] {colr.Colr().hex('#04e762', 'Arkose FunCaptcha')} "
                        f"{colr.Colr().hex('#adaaad', variant.upper())} "
                        f"{colr.Colr().hex('#b388eb', json.dumps(answers_found))}\n")
                sys.stdout.flush()
                headers: dict = {
                    'accept': '*/*',
                    'Accept-Language': language,
                    'cache-control': 'no-cache',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': self.arkose_api_url,
                    'referer': f'{ref}?session={full_token.replace("|", "&")}',
                    **extra_headers,
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': fingerprint_data.agent,
                    'x-requested-with': 'XMLHttpRequest',
                }
                data = {
                    'session_token': session_token,
                    'game_token': game_token,
                    'sid': region,
                    'guess': crypt.encrypt(json.dumps(answers), session_token),
                    "render_type": render_type,
                    'analytics_tier': '40',
                    'bio': "",
                }
                response = self.post(f'{self.arkose_api_url}/fc/ca/', headers=headers,
                                     data=data).json()
                if response.get('solved'):
                    for elem in hashes:
                        audio_database.save_valid_audio(variant, elem[0], elem[1])
                    return {
                        "waves": len(audio_urls),
                        "variant": variant.upper(),
                        "type": game_type,
                        "token": full_token,
                        "solved": True
                    }
                elif response.get('solved') is not None:
                    return {
                        "waves": len(audio_urls),
                        "variant": variant.upper(),
                        "type": game_type,
                        "token": full_token,
                        "solved": False
                    }
