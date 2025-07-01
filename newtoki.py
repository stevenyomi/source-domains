import re

from common import get_domain, write_result

def main() -> None:
    res = get_domain('newtoki.link').raise_for_status()

    number = re.findall(r'https://newtoki(\d+)\.com', res.text)[-1]

    write_result('newtoki.txt', number, f'NewToki {number}')
