import httpx
import re

from tenacity import retry, stop_after_attempt

from common import write_result

@retry(stop=stop_after_attempt(5))
def make_request(client: httpx.Client):
    res = client.get('https://t.me/s/newtoki5')
    if res.status_code != 200:
        raise Exception(f'HTTP {res.status_code}')
    return res

def main() -> None:
    with httpx.Client() as client:
        res = make_request(client)

    number = re.findall(r'https://newtoki(\d+)\.com', res.text)[-1]

    write_result('newtoki.txt', number, f'NewToki {number}')

main()
