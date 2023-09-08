OVERWRITE_IP: dict = {
    b"www.roblox.com": b"[2607:f798:d04:182::1c3d]"
    # b"login.live.com": b"[2603:1026:3000::]",
    # b"login.microsoftonline.com": b"[2603:1026:3000::]",
    # b"paymentinstruments.mp.microsoft.com": b"[2620:1ec:bdf::48]",
}


def overwrite(host) -> str:
    return OVERWRITE_IP.get(host, host)
