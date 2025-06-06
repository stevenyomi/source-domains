import re

from common import http_get, write_result

def main() -> None:
    res = http_get('https://t.me/s/newtoki5')

    number = re.findall(r'https://newtoki(\d+)\.com', res.text)[-1]

    write_result('newtoki.txt', number, f'NewToki {number}')
