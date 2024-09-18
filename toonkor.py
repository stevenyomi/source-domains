import re

import idna
from httpx import Client

from common import extract_location, get_domain, write_result


def main() -> None:
    decode = idna.decode

    def wrapped_decode(*args, **kwargs):
        try:
            return decode(*args, **kwargs)
        except Exception:
            return args[0]

    idna.decode = decode

    with Client() as client:
        response = get_domain(client, "xn--yq5bv6mzmcca.org")
        assert response.is_redirect
        domain = extract_location(response)

    number = re.match(r"toonkor(\d+)\.com", domain).group(1)

    write_result("toonkor.txt", number, f"Toonkor {number}")


main()
