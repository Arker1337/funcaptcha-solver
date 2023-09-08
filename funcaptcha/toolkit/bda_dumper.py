import base64
import time
import traceback

from funcaptcha.utilities.encryption import crypt


def program():
    try:
        bda_decoded = base64.b64decode(input("BDA -> ").encode()).decode()
        ua_key = input("User Agent -> ")
        timestamp = int(time.time())
        timestamp -= timestamp % 21600
        ua_key2 = f"{ua_key}{timestamp}"
        print(crypt.decrypt(bda_decoded, ua_key2).decode())
        input("Press any key to return to the main menu.")
    except Exception as ex:
        traceback.print_exc()
        print("The bda you provided is invalid/expired or you supplied the wrong user agent.")
        time.sleep(4)


if __name__ == '__main__':
    program()
