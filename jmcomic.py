import re

from common import http_get, write_result

def main() -> None:
    res = http_get('https://jmcomicone-xyz.translate.goog/?_x_tr_sl=auto&_x_tr_tl=zh-TW', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    text = (text := res.text)[(index := text.index('<body>') + 6) : text.index('<script>', index)]
    text = text.replace('&nbsp;', ' ')
    text = re.sub(r'<.+?>', ' ', text)
    domains = re.findall(r'[-\w]+\.[-\w.]+', text)
    assert domains[:4] == ['18comic.vip', '18comic.org', 'jmcomic.me', 'jmcomic1.me']
    end = domains.index('jm365.work')
    assert end > 4
    domains = ','.join(domains[4:end])


    write_result('jmcomic.txt', domains, f'JM {domains}')

main()
