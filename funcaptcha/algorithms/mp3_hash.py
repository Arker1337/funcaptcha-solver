from hashlib import md5


def hash_mp3(input_data: bytes) -> str:
    data: list[bytes] = [
        b"Anti-Retard String, Solver by Dort & bebebebebe ",
        b"The purpose of this string is to make sure that there will ",
        b"always be a fingerprint in their code if someone ever gets ",
        b"our hashes\x07nigga balls 144p\x08\x02\x00\x03\x00\x01\x20 ",
        # strip off junk data regions at both ends.
        input_data[128:len(input_data) - 128]
    ]
    return md5(b"".join(data)).hexdigest()
