import random

from common.databases import global_redis_database_fc_101


def save_valid_audio(variant: str, audio_hash: str, answer: int) -> None:
    global_redis_database_fc_101.set(f"{variant}:{audio_hash}", answer)


def check_valid_audio(audio_hash: str, variant: str) -> tuple[int, bool]:
    try:
        audio_state = global_redis_database_fc_101.get(f"{variant}:{audio_hash}").decode()
        return int(audio_state), True
    except Exception:
        pass
    return random.randint(1, 3), False
