import re

from common import http_get, write_result


def main() -> None:
    res = http_get("https://t.me/s/new_toonkor")

    number = re.findall(r"https://toonkor(\d+)\.com", res.text)[-1]

    write_result("toonkor.txt", number, f"Toonkor {number}")


main()
