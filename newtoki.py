import httpx
import re

try:
    res = httpx.get('https://t.me/s/newtoki5')
    if res.status_code != 200:
        raise Exception(f'HTTP {res.status_code}')

    number = re.findall(r'https://newtoki(\d+)\.com', res.text)[-1]

    with open('newtoki.txt', 'w') as f:
        f.write(number)

    with open('.git/COMMIT_EDITMSG', 'w') as f:
        f.write(f'NewToki {number}')

except BaseException as e:
    print(f'::error ::{e}')
    exit(1)
