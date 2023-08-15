import re
import os

import httpx

PROXY = os.getenv('JM_PROXY') # Proxy for https://jmcomic2.bet/

try:
    res = httpx.get(PROXY)
    if res.status_code != 200:
        raise Exception(f'HTTP {res.status_code}')

    text = res.text.partition('<script>')[0]
    text = text.replace('&nbsp;', ' ')
    text = re.sub(r'<.+?>', ' ', text)
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
