import base64
import json
import os
import random
import secrets
import time
import warnings
from io import BytesIO
from typing import Union
import mmh3
import numpy as np
from PIL import Image
from random_user_agent.user_agent import UserAgent

from .templates.outlook import generate_bda as outlook
from .templates.roblox_login import generate_bda as roblox_login
from .templates.roblox_register import generate_bda as roblox_register
from ..utilities.encryption import crypt

warnings.filterwarnings("ignore")
x64hash128 = lambda key, seed=0: mmh3.hash_bytes(key.encode(), seed).hex()
ua = UserAgent()

pixel_ratios = [
    0.5,
    0.75,
    1,
    1.25,
    1.5,
    1.75,
    2,
    2.25,
    2.5,
    2.75,
    3,
    3.25,
    random.uniform(1.06, 1.24),
]
gpu_models = [
    260,
    265,
    270,
    275,
    280,
    285,
    310,
    450,
    460,
    470,
    475,
    480,
    530,
    550,
    570,
    575,
    580,
    590,
    610,
    630,
    640,
    645,
    650,
    660,
    670,
    680,
    690,
    710,
    740,
    745,
    750,
    760,
    770,
    780,
    950,
    960,
    970,
    980,
    1010,
    1030,
    1050,
    1070,
    1080,
    2050,
    2060,
    2070,
    2080,
    3050,
    3060,
    3070,
    3080,
    3090,
    4050,
    4060,
    4070,
    4080,
    4090,
    *[random.randint(260, 69420) for x in range(random.randint(1, 25))],
]
languages = [
    "af",
    "af-ZA",
    "ar",
    "ar-AE",
    "ar-BH",
    "ar-DZ",
    "ar-EG",
    "ar-IQ",
    "ar-JO",
    "ar-KW",
    "ar-LB",
    "ar-LY",
    "ar-MA",
    "ar-OM",
    "ar-QA",
    "ar-SA",
    "ar-SY",
    "ar-TN",
    "ar-YE",
    "az",
    "az-AZ",
    "az-AZ",
    "be",
    "be-BY",
    "bg",
    "bg-BG",
    "bs-BA",
    "ca",
    "ca-ES",
    "cs",
    "cs-CZ",
    "cy",
    "cy-GB",
    "da",
    "da-DK",
    "de",
    "de-AT",
    "de-CH",
    "de-DE",
    "de-LI",
    "de-LU",
    "dv",
    "dv-MV",
    "el",
    "el-GR",
    "en",
    "en-AU",
    "en-BZ",
    "en-CA",
    "en-CB",
    "en-GB",
    "en-IE",
    "en-JM",
    "en-NZ",
    "en-PH",
    "en-TT",
    "en-US",
    "en-ZA",
    "en-ZW",
    "eo",
    "es",
    "es-AR",
    "es-BO",
    "es-CL",
    "es-CO",
    "es-CR",
    "es-DO",
    "es-EC",
    "es-ES",
    "es-ES",
    "es-GT",
    "es-HN",
    "es-MX",
    "es-NI",
    "es-PA",
    "es-PE",
    "es-PR",
    "es-PY",
    "es-SV",
    "es-UY",
    "es-VE",
    "et",
    "et-EE",
    "eu",
    "eu-ES",
    "fa",
    "fa-IR",
    "fi",
    "fi-FI",
    "fo",
    "fo-FO",
    "fr",
    "fr-BE",
    "fr-CA",
    "fr-CH",
    "fr-FR",
    "fr-LU",
    "fr-MC",
    "gl",
    "gl-ES",
    "gu",
    "gu-IN",
    "he",
    "he-IL",
    "hi",
    "hi-IN",
    "hr",
    "hr-BA",
    "hr-HR",
    "hu",
    "hu-HU",
    "hy",
    "hy-AM",
    "id",
    "id-ID",
    "is",
    "is-IS",
    "it",
    "it-CH",
    "it-IT",
    "ja",
    "ja-JP",
    "ka",
    "ka-GE",
    "kk",
    "kk-KZ",
    "kn",
    "kn-IN",
    "ko",
    "ko-KR",
    "kok",
    "kok-IN",
    "ky",
    "ky-KG",
    "lt",
    "lt-LT",
    "lv",
    "lv-LV",
    "mi",
    "mi-NZ",
    "mk",
    "mk-MK",
    "mn",
    "mn-MN",
    "mr",
    "mr-IN",
    "ms",
    "ms-BN",
    "ms-MY",
    "mt",
    "mt-MT",
    "nb",
    "nb-NO",
    "nl",
    "nl-BE",
    "nl-NL",
    "nn-NO",
    "ns",
    "ns-ZA",
    "pa",
    "pa-IN",
    "pl",
    "pl-PL",
    "ps",
    "ps-AR",
    "pt",
    "pt-BR",
    "pt-PT",
    "qu",
    "qu-BO",
    "qu-EC",
    "qu-PE",
    "ro",
    "ro-RO",
    "ru",
    "ru-RU",
    "sa",
    "sa-IN",
    "se",
    "se-FI",
    "se-FI",
    "se-FI",
    "se-NO",
    "se-NO",
    "se-NO",
    "se-SE",
    "se-SE",
    "se-SE",
    "sk",
    "sk-SK",
    "sl",
    "sl-SI",
    "sq",
    "sq-AL",
    "sr-BA",
    "sr-BA",
    "sr-SP",
    "sr-SP",
    "sv",
    "sv-FI",
    "sv-SE",
    "sw",
    "sw-KE",
    "syr",
    "syr-SY",
    "ta",
    "ta-IN",
    "te",
    "te-IN",
    "th",
    "th-TH",
    "tl",
    "tl-PH",
    "tn",
    "tn-ZA",
    "tr",
    "tr-TR",
    "tt",
    "tt-RU",
    "ts",
    "uk",
    "uk-UA",
    "ur",
    "ur-PK",
    "uz",
    "uz-UZ",
    "uz-UZ",
    "vi",
    "vi-VN",
    "xh",
    "xh-ZA",
    "zh",
    "zh-CN",
    "zh-HK",
    "zh-MO",
    "zh-SG",
    "zh-TW",
    "zu",
    "zu-ZA",
]
warnings.filterwarnings("ignore")


def get_fp():
    screen = random.randint(1920, 7680), random.randint(720, 5120)
    avail_screen = random.randint(screen[0] - 250, screen[0]), random.randint(
        screen[1] - 100, screen[1]
    )
    timezone_offset = random.choice(
        [-420, -360, -300, -240, -120, -60, 0, 60, 120, 240, 300, 360, 420]
    )
    gpu_model = random.choice(gpu_models)
    valid_exts = "ANGLE_instanced_arrays;EXT_blend_minmax;EXT_color_buffer_half_float;EXT_disjoint_timer_query;EXT_float_blend;EXT_frag_depth;EXT_shader_texture_lod;EXT_texture_compression_bptc;EXT_texture_compression_rgtc;EXT_texture_filter_anisotropic;EXT_sRGB;KHR_parallel_shader_compile;OES_element_index_uint;OES_fbo_render_mipmap;OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;WEBGL_color_buffer_float;WEBGL_compressed_texture_s3tc;WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBGL_multi_draw".split(
        ";"
    )
    valid_exts = random.sample(valid_exts, random.randint(3, len(valid_exts)))
    for i in range(random.randint(1, 24)):
        valid_exts.append(secrets.token_urlsafe(random.randint(3, 12)))
    fake_vendor = secrets.token_urlsafe(random.randint(3, 8))
    return {
        "webgl": {
            "webgl_extensions": ";".join(valid_exts),
            "webgl_renderer": secrets.token_urlsafe(random.randint(1, 19)),
            "webgl_vendor": secrets.token_urlsafe(random.randint(1, 15)),
            "webgl_version": secrets.token_urlsafe(random.randint(1, 17)),
            "webgl_shading_language_version": secrets.token_urlsafe(
                random.randint(1, 11)
            ),
            "webgl_aliased_line_width_range": f"[{random.randint(1, 45)}, {random.randint(1, 25)}]",
            "webgl_aliased_point_size_range": f"[{random.randint(1, 32215)}, {random.randint(1, 32215)}]",
            "webgl_antialiasing": random.choice(
                ["yes", "no", secrets.token_urlsafe(random.randint(4, 9))]
            ),
            "webgl_bits": ",".join([str(random.randint(1, 24)) for _ in range(6)]),
            "webgl_max_params": ",".join(
                [str(random.randint(1, 4095)) for _ in range(random.randint(4, 18))]
            ),
            "webgl_max_viewport_dims": f"[{random.randint(1, 22215)}, {random.randint(1, 22215)}]",
            "webgl_unmasked_vendor": f"{secrets.token_urlsafe(random.randint(3, 5))} ({fake_vendor})",
            "webgl_unmasked_renderer": f"ANGLE ({fake_vendor}, {fake_vendor} {secrets.token_urlsafe(3)} {gpu_model} Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "webgl_vsf_params": ",".join(
                [str(random.randint(1, 32)) for _ in range(random.randint(7, 22))]
            ),
            "webgl_vsi_params": ",".join(
                [str(random.randint(1, 256)) for _ in range(random.randint(9, 17))]
            ),
            "webgl_fsf_params": ",".join(
                [str(random.randint(1, 128)) for _ in range(random.randint(10, 29))]
            ),
            "webgl_fsi_params": ",".join(
                [str(random.randint(1, 56)) for _ in range(random.randint(4, 31))]
            ),
        },
        "fe": {
            "DNT": random.choice(["unknown", "1", "unspecified"]),
            "L": random.choice(languages),
            "D": str(random.randint(8, 24)),
            "PR": str(random.choice(pixel_ratios)),
            "S": f"{screen[0]};{screen[1]}",
            "AS": f"{avail_screen[0]};{avail_screen[1]}",
            "TO": str(timezone_offset),
            "SS": "true",
            "LS": "true",
            "IDB": "true",
            "B": "false",
            "ODB": "true",
            "CPUC": "unknown",
            "PK": "Win32",
            "CFP": secrets.token_urlsafe(26),
            "FR": "false",
            "FOS": "false",
            "FB": "false",
            "JSF": "",
            "P": secrets.token_urlsafe(41),
            "T": f"0;false;false",
            "H": str(random.randint(1, 256)),
            "SWF": "false",
        },
    }


def generate_bda(fingerprint, cap_url):
    if cap_url == "roblox_register":
        bda = roblox_register(fingerprint, cap_url)
    elif cap_url == "roblox_login":
        bda = roblox_login(fingerprint, cap_url)
    else:
        bda = outlook(fingerprint, cap_url)
    return bda


class BDA:
    def __init__(self, fingerprint: str, agent: str, raw_bda: dict, cfp: str):
        self.cfp = cfp
        self.fingerprint = fingerprint
        self.agent = agent
        self.raw_bda = raw_bda


def create_webgl(fingerprint):
    webgl_extensions = fingerprint["webgl"]["webgl_extensions"]
    webgl_extensions_hash = x64hash128(webgl_extensions)
    webgl = [
        {"key": "webgl_extensions", "value": webgl_extensions},
        {"key": "webgl_extensions_hash", "value": webgl_extensions_hash},
    ]
    xd = []
    for x, y in fingerprint["webgl"].items():
        if x != "webgl_extensions":
            webgl.append({"key": x, "value": y})
    for k, v in fingerprint["webgl"].items():
        if v is None:
            xd.append("")
        else:
            xd.append(v)
    webgl.append({"key": "webgl_hash_webgl", "value": x64hash128(",".join(xd))})
    return webgl


def random_valid_img():
    imarray = np.random.rand(15, 15, 3) * 255
    im = Image.fromarray(imarray.astype("uint8")).convert("RGBA")
    bio = BytesIO()
    im.save(bio, "png")
    val = bio.getvalue()
    del bio
    return f"canvas winding:yes~canvas fp:data:image/png;base64,{base64.b64encode(val).decode()}"


def cfp_hash(string_in: str) -> int:
    int1 = np.int32(0)
    for int2 in range(len(string_in)):
        int3 = np.int32(ord(string_in[int2]))
        int1 = np.int32((int1 << 5) - int1 + int3)
        int1 = np.bitwise_and(int1, np.int32(-1))
    return int1.item()


def generate_enhanced_fp(fingerprint, cap_url):
    webgl_json = create_webgl(fingerprint)
    other_json = generate_bda(fingerprint, cap_url)
    for __f in other_json:
        webgl_json.append(__f)
    return webgl_json


def generate_fe(fingerprint):
    fe = fingerprint["fe"]
    fe["P"] = fe["P"].replace(
        "application/pdf~pdf,text/pdf~pdf,", "application/pdf~pdf,text/pdf~pdf;"
    )
    return fe


def get_f_hash(fe):
    fe_value_array = []
    for x in fe:
        y = fe[x]
        fe_value_array.append(y)
    fe_string = "~~~".join(fe_value_array)
    return x64hash128(fe_string, 31)


def get_ife_hash(fe):
    fe_value_array = []
    for x in fe:
        y = fe[x]
        fe_value_array.append(x + ":" + y)
    fe_string = (
        ",".join(fe_value_array)
        .replace("::Portable Document Format::application/pdf~pdf,text/pdf~pdf", "")
        .replace(";", ",")
    )
    return x64hash128(fe_string, 38)


def get_fe_array(fe):
    fe_value_array = []
    for x in fe:
        y = fe[x]
        fe_value_array.append(
            f"{x}:{y}".replace(
                "::Portable Document Format::application/pdf~pdf,text/pdf~pdf", ""
            ).replace(";", ",")
        )
    return fe_value_array


def get_bda(fingerprint: dict, cap_url: str) -> list:
    enhanced_fp = generate_enhanced_fp(fingerprint, cap_url)
    fe = generate_fe(fingerprint)
    f = get_f_hash(fe)
    fe["CFP"] = str(cfp_hash(secrets.token_urlsafe(64)))
    ife = get_ife_hash(fe)
    fe_array = get_fe_array(fe)
    timestamp: int = int(time.time())
    bda_json = [
        {"key": "api_type", "value": "js"},
        {"key": "p", "value": 1},
        {"key": "f", "value": f},
        {
            "key": "wh",
            "value": f"{secrets.token_hex(16)}|72627afbfd19a741c7da1732218301ac",
        },
        {"key": "n", "value": str(base64.b64encode(str(timestamp).encode()).decode())},
        {"key": "enhanced_fp", "value": enhanced_fp},
        {"key": "fe", "value": fe_array},
        {"key": "ife_hash", "value": ife},
        {"key": "cs", "value": 1},
        {
            "key": "jsbd",
            "value": '{"HL":'
            + str(random.randint(2, 4))
            + ',"NCE":true,"DT":"","NWD":"false","DOTO":1,"DMTO":1}',
        },
    ]
    return bda_json


def get_fingerprint(
    site: str,
    custom_user_agent: Union[str, None] = None,
    attempt_easy_challenge: bool = True,
) -> BDA:
    d = random.uniform(120, 1000)
    fingerprint = get_fp()
    if attempt_easy_challenge:
        agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:12.2.1) Gecko/20120616 Firefox/12.2.1-x64 PaleMoon/12.2.1-x64"
    elif custom_user_agent:
        agent = custom_user_agent
    else:
        agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{d} (KHTML, like Gecko) Chrome/{random.randint(102, 105)}.0.0.0 Safari/{d}"
    bda_json = get_bda(fingerprint, site)
    timestamp: int = int(time.time())
    timeframe: int = round(timestamp - timestamp % 21600)
    bda_json[4]["value"] = str(base64.b64encode(str(timestamp).encode()).decode())
    fingerprint_key: str = f"{agent}{timeframe}"
    return BDA(
        base64.b64encode(
            crypt.encrypt(
                json.dumps(bda_json, separators=(",", ":")), fingerprint_key
            ).encode()
        ).decode(),
        agent,
        fingerprint,
        fingerprint.get("fe").get("CFP"),
    )
