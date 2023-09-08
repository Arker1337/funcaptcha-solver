import modded_httpx

_API_ = 'https://api.nopecha.com/'
_KEY_: str = "I-AF7TF8CVG2R9"


def classify(image_data_b64: str, question: str, nopecha_key: str = _KEY_):
    job_id = modded_httpx.post(_API_, json={
        'type': 'funcaptcha',
        'image_data': [image_data_b64],
        'task': question,
        'key': nopecha_key,
    }).json().get('data')
    resp: list = modded_httpx.get(f"{_API_}?key={nopecha_key}&id={job_id}").json().get("data")
    return resp.index(True)
