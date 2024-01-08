import re

import httpx

try:
    res = httpx.get('https://jcomic--cn-vip.translate.goog/?_x_tr_sl=auto&_x_tr_tl=zh-TW', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
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
