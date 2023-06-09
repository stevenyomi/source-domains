import re
import os

import httpx

PROXY = os.getenv('JM_PROXY')

try:
    res = httpx.get(PROXY + 'https://jmcomic2.bet/')
    if res.status_code != 200:
        raise Exception(f'HTTP {res.status_code}')

    text = re.sub(r'<.+?>', ' ', res.text.replace('&nbsp;', ' '))
    domains = re.findall(r'[-\w]+\.[-\w.]+', text)
    assert domains[:4] == ['18comic.vip', '18comic.org', 'jmcomic.me', 'jmcomic1.me']
    end = domains.index('jm365.work')
    assert end > 4
    domains = ','.join(domains[4:end])

    with open('jmcomic.txt', 'w') as f:
        f.write(domains)

    with open('.git/COMMIT_EDITMSG', 'w') as f:
        f.write(f'JM {domains}')

except BaseException as e:
    print(f'::error ::{e}')
    exit(1)
