import json
import random
import secrets


def generate_bda(fingerprint, cap_url):
    skip_res: bool = random.randint(0, 1) == 1
    target_len = random.randint(4, 100)
    keys = [secrets.token_urlsafe(14) for _ in range(target_len)]
    values = ["probably" for _ in range(target_len)]
    audio_fp = {
        key: value for key, value in zip(keys, values)
    }
    return [
        {
            "key": "user_agent_data_brands",
            "value": f"{secrets.token_urlsafe(14)},Google Chrome,Not:A-Brand"
        },
        {
            "key": "user_agent_data_mobile",
            "value": False
        },
        {
            "key": "navigator_connection_downlink",
            "value": round(random.uniform(1, 100), 3)
        },
        {
            "key": "navigator_connection_downlink_max",
            "value": None
        },
        {
            "key": "network_info_rtt",
            "value": random.randint(50, 111111)
        },
        {
            "key": "network_info_save_data",
            "value": False
        },
        {
            "key": "network_info_rtt_type",
            "value": None
        },
        {
            "key": "screen_pixel_depth",
            "value": int(fingerprint["fe"]["D"])
        },
        {
            "key": "navigator_device_memory",
            "value": random.randint(1, 8)
        },
        {
            "key": "navigator_languages",
            "value": fingerprint['fe']['L'] + "," + fingerprint['fe']['L'].split("-")[0]
        },
        {
            "key": "window_inner_width",
            "value": 0 if skip_res else int(fingerprint["fe"]["AS"].split(";")[0])
        },
        {
            "key": "window_inner_height",
            "value": 0 if skip_res else int(fingerprint["fe"]["AS"].split(";")[1])
        },
        {
            "key": "window_outer_width",
            "value": int(fingerprint["fe"]["AS"].split(";")[0])
        },
        {
            "key": "window_outer_height",
            "value": int(fingerprint["fe"]["AS"].split(";")[1])
        },
        {
            "key": "browser_detection_firefox",
            "value": False
        },
        {
            "key": "browser_detection_brave",
            "value": False
        },
        {
            "key": "audio_codecs",
            "value": json.dumps(audio_fp, separators=(",", ";"))
        },
        {
            "key": "video_codecs",
            "value": "{\"ogg\":\"probably\",\"h264\":\"probably\",\"webm\":\"probably\",\"mpeg4v\":\"\",\"mpeg4a\":\"\",\"theora\":\"\"}"
        },
        {
            "key": "media_query_dark_mode",
            "value": False
        },
        {
            "key": "headless_browser_phantom",
            "value": False
        },
        {
            "key": "headless_browser_selenium",
            "value": False
        },
        {
            "key": "headless_browser_nightmare_js",
            "value": False
        },
        {
            "key": "document__referrer",
            "value": "https://www.roblox.com/"
        },
        {
            "key": "window__ancestor_origins",
            "value": [
                "https://www.roblox.com",
                "https://www.roblox.com"
            ]
        },
        {
            "key": "window__tree_index",
            "value": [
                0,
                0
            ]
        },
        {
            "key": "window__tree_structure",
            "value": "[[[]]]"
        },
        {
            "key": "window__location_href",
            "value": "https://roblox-api.arkoselabs.com/v2/1.5.4/enforcement.cd12da708fe6cbe6e068918c38de2ad9.html#A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F"
        },
        {
            "key": "client_config__sitedata_location_href",
            "value": "https://www.roblox.com/arkose/iframe"
        },
        {
            "key": "client_config__surl",
            "value": "https://roblox-api.arkoselabs.com"
        },
        {
            "key": "mobile_sdk__is_sdk"
        },
        {
            "key": "client_config__language",
            "value": fingerprint['fe']['L']
        },
        {
            "key": "navigator_battery_charging",
            "value": True
        },
        {
            "key": "audio_fingerprint",
            "value": str(round(random.uniform(123.0, 124.08), 14))
        }
    ]
