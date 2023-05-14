import os
import re

import httpx

link = 'https://www.wnacglink.top/' if os.getenv('CI') else 'https://wn01.ru/'
regex = re.compile(r'<a href="(https?://([.\w]+))/?" target="_blank"><i>\2</i></a>')

try:
    res = httpx.get(link)
    if res.status_code != 200:
        raise Exception(f'HTTP {res.status_code}')

    urls, domains = [], []
    for match in regex.finditer(res.text):
        urls.append(match.group(1))
        domains.append(match.group(2).removeprefix('www.'))

    assert len(urls) > 0

    with open('wnacg.txt', 'w') as f:
        f.write(','.join(urls))

    with open('.git/COMMIT_EDITMSG', 'w') as f:
        f.write('WNACG ' + ','.join(domains))

except BaseException as e:
    print(f'::error ::{e}')
    exit(1)
