import re

import idna

from common import extract_location, get_domain, write_result


def main() -> None:
    decode = idna.decode

    def wrapped_decode(*args, **kwargs):
        try:
            return decode(*args, **kwargs)
        except Exception:
            return args[0]

    idna.decode = wrapped_decode

    if True:
        response = get_domain("xn--yq5bv6mzmcca.org")
        assert response.is_redirect
        domain = extract_location(response)

    number = re.match(r"tkor(\d+)\.com", domain).group(1)

    write_result("toonkor.txt", number, f"Toonkor {number}")
