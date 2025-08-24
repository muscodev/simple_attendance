from fastapi import Request


def ip_from_request(request: Request):
    "Return ip address"
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]  # In case of multiple proxies
    else:
        ip = request.client.host
    return ip
