from tls_client import Session
from re import findall
from json import loads, dumps, load
from datetime import datetime
from utils.crypto import Crypto
from random import randint, choice
from names import get_first_name, get_last_name
from os import urandom
from time import time
from threading import Thread
import random, secrets, multiprocessing

from funcaptcha import ArkoseSession


class Funcaptcha:
    def getKey() -> str:
        while True:
            try:
                data = ArkoseSession(
                    "https://iframe.arkoselabs.com",
                    random.choice(
                        [
                            # "B5B07C8C-F93F-44A8-A353-4A47B8AD5238",
                            "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
                            # "EA4B65CB-594A-438E-B4B5-D0DBA28C9334",
                            # "DF58DD3B-DFCC-4502-91FA-EDC0DC385CFF",
                            # "2F4F0B28-BC94-4271-8AD7-A51662E3C91C",
                            # "73BEC076-3E53-30F5-B1EB-84F494D43DBA",
                            # "3117BF26-4762-4F5A-8ED9-A85E69209A46",
                            # "69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC",
                            # "A5A70501-FCDE-4065-AF18-D9FAF06EF479"
                        ]
                    ),
                    "https://client-api.arkoselabs.com",
                    "https://signup.live.com",
                    {"blob": secrets.token_urlsafe(32)},
                    "http://wfipdEyz:sdIeqcCssvapoLVI@delta.proxies.cx:47212",
                    True,
                ).solve(False, False)

                if data.get("solved"):
                    return data.get("token")
            except:
                pass


class Outlook:
    def __init__(this, proxy: str = None):
        this.client = Session(client_identifier="chrome_108")
        this.client.proxies = (
            {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        )

        this.Key = None
        this.randomNum = None
        this.SKI = None
        this.uaid = None
        this.tcxt = None
        this.apiCanary = None
        this.encAttemptToken = ""
        this.dfpRequestId = ""

        this.siteKey = "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA"
        this.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"

        this.__start__ = this.__init_client()
        this.account_info = this.__account_info()

        this.cipher = Crypto.encrypt(
            this.account_info["password"], this.randomNum, this.Key
        )

    @staticmethod
    def log(message: str):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def __init_client(this):
        content = this.client.get(
            "https://signup.live.com/signup?lic=1",
            headers={
                "host": "signup.live.com",
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "connection": "keep-alive",
                "user-agent": this.userAgent,
            },
        )

        this.Key, this.randomNum, this.SKI = findall(
            r'Key="(.*?)"; var randomNum="(.*?)"; var SKI="(.*?)"', content.text
        )[0]
        json_data = loads(
            findall(r't0=([\s\S]*)w\["\$Config"]=', content.text)[0].replace(";", "")
        )

        this.uaid = json_data["clientTelemetry"]["uaid"]
        this.tcxt = json_data["clientTelemetry"]["tcxt"]
        this.apiCanary = json_data["apiCanary"]

    def __handle_error(this, code: str) -> str:
        errors = {
            "403": "Bad Username",
            "1040": "SMS Needed",
            "1041": "Enforcement Captcha",
            "1042": "Text Captcha",
            "1043": "Invalid Captcha",
            "1312": "Captcha Error",
            "450": "Daily Limit Reached",
            "1304": "OTP Invalid",
            "1324": "Verification SLT Invalid",
            "1058": "Username Taken",
            "1117": "Domain Blocked",
            "1181": "Reserved Domain",
            "1002": "Incorrect Password",
            "1009": "Password Conflict",
            "1062": "Invalid Email Format",
            "1063": "Invalid Phone Format",
            "1039": "Invalid Birth Date",
            "1243": "Invalid Gender",
            "1240": "Invalid first name",
            "1241": "Invalid last name",
            "1204": "Maximum OTPs reached",
            "1217": "Banned Password",
            "1246": "Proof Already Exists",
            "1184": "Domain Blocked",
            "1185": "Domain Blocked",
            "1052": "Email Taken",
            "1242": "Phone Number Taken",
            "1220": "Signup Blocked",
            "1064": "Invalid Member Name Format",
            "1330": "Password Required",
            "1256": "Invalid Email",
            "1334": "Eviction Warning Required",
            "100": "Bad Register Request",
        }

        return errors[code]

    def __account_info(this) -> dict:
        token = urandom(3).hex()
        first_name = get_first_name()
        last_name = get_last_name()
        email = f"{first_name}.{last_name}.{token}@outlook.com".lower()
        password = "!!VichyOnTop1337"

        return {
            "password": password,
            "CheckAvailStateMap": [f"{email}:undefined"],
            "MemberName": email,
            "FirstName": first_name,
            "LastName": last_name,
            "BirthDate": f"{randint(1, 27)}:0{randint(1, 9)}:{randint(1969, 2000)}",
        }

    def __base_headers(this):
        return {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "canary": this.apiCanary,
            "content-type": "application/json",
            "dnt": "1",
            "hpgid": f"2006{randint(10, 99)}",
            "origin": "https://signup.live.com",
            "pragma": "no-cache",
            "scid": "100118",
            "sec-ch-ua": '" Not A;Brand";v="107", "Chromium";v="96", "Google Chrome";v="96"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "tcxt": this.tcxt,
            "uaid": this.uaid,
            "uiflvr": "1001",
            "user-agent": this.userAgent,
            "x-ms-apitransport": "xhr",
            "x-ms-apiversion": "2",
            "referrer": "https://signup.live.com/?lic=1",
        }

    def __base_payload(this, captcha_solved: bool) -> dict:
        payload = {
            **this.account_info,
            "RequestTimeStamp": str(datetime.now()).replace(" ", "T")[:-3] + "Z",
            "EvictionWarningShown": [],
            "UpgradeFlowToken": {},
            "MemberNameChangeCount": 1,
            "MemberNameAvailableCount": 1,
            "MemberNameUnavailableCount": 0,
            "CipherValue": this.cipher,
            "SKI": this.SKI,
            "Country": "CA",
            "AltEmail": None,
            "IsOptOutEmailDefault": True,
            "IsOptOutEmailShown": True,
            "IsOptOutEmail": True,
            "LW": True,
            "SiteId": 68692,
            "IsRDM": 0,
            "WReply": None,
            "ReturnUrl": None,
            "SignupReturnUrl": None,
            "uiflvr": 1001,
            "uaid": this.uaid,
            "SuggestedAccountType": "OUTLOOK",
            "SuggestionType": "Locked",
            "encAttemptToken": this.encAttemptToken,
            "dfpRequestId": this.dfpRequestId,
            "scid": 100118,
            "hpgid": 201040,
        }

        if captcha_solved:
            cap_token = Funcaptcha.getKey()
            Outlook.log(f"solved captcha: [{cap_token[:100]}...]")

            payload.update(
                {
                    "HType": "enforcement",
                    "HSol": cap_token,
                    "HPId": this.siteKey,
                }
            )

        return payload

    def register_account(this, captcha_solved: bool = False) -> dict and str:
        try:
            for _ in range(3):
                try:
                    response = this.client.post(
                        "https://signup.live.com/API/CreateAccount?lic=1",
                        json=this.__base_payload(captcha_solved),
                        headers=this.__base_headers(),
                    )

                    """h = this.__base_headers()
                    h["action"] = "SetConsumerMailbox"
                    resp = this.client.post(
                        "https://outlook.live.com/owa/0/service.svc",
                        params={
                            "action": "SetConsumerMailbox",
                            "app": "Mail",
                            "n": "70",
                        },
                        headers=h,
                    )
                    print(resp.status_code, resp.text)"""

                    Outlook.log(f"register resp:  [{str(response.json())[:100]}...]")
                    break

                except Exception as e:
                    Outlook.log(f"http error: [{e}]")
                    continue

            error = response.json().get("error")
            if error:
                code = error.get("code")
                if "1041" in code:
                    error_data = loads(error.get("data"))

                    this.encAttemptToken = error_data["encAttemptToken"]
                    this.dfpRequestId = error_data["dfpRequestId"]

                    return this.register_account(True)

                else:
                    return {}, this.__handle_error(code)

            else:
                return this.account_info, "Success"

        except Exception as e:
            return {}, str(e)


def register_loop(proxies: list):
    while True:
        try:
            start = time()
            outlook = Outlook(choice(proxies))
            account, status = outlook.register_account()
            stop = time() - start

            if status == "Success":
                Outlook.log(
                    f'registered acc: [{account["MemberName"]}:...] {round(stop, 2)}s'
                )
                with open("./data/accounts.txt", "a") as f:
                    f.write(f'{account["MemberName"]}:{account["password"]}\n')
            else:
                Outlook.log(f"register error: [{status}] {round(stop, 2)}s")
        except:
            pass


if __name__ == "__main__":
    proxies = open("./data/proxies.txt").read().splitlines()
    config = load(open("./data/config.json"))

    for _ in range(config["threads"]):
        Thread(target=register_loop, args=(proxies,)).start()