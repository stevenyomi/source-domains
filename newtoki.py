import httpx
import re

from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(5))
def make_request(client: httpx.Client):
    res = client.get('https://t.me/s/newtoki5')
    if res.status_code != 200:
        raise Exception(f'HTTP {res.status_code}')
    return res

try:
    with httpx.Client() as client:
        res = make_request(client)

    number = re.findall(r'https://newtoki(\d+)\.com', res.text)[-1]

    with open('newtoki.txt', 'w') as f:
        f.write(number)

    with open('.git/COMMIT_EDITMSG', 'w') as f:
        f.write(f'NewToki {number}')

except BaseException as e:
    print(f'::error ::{e}')
    exit(1)
