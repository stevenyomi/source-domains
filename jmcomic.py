import re
from os import getenv

from httpx import URL

from common import CLIENT, extract_location, get_domain, write_result


def retry_get(url: str):
    attempts = 5
    while True:
        try:
            if (res := CLIENT.get(url)).status_code == 430:
                raise Exception(f'HTTP {res.status_code}')
            return res
        except Exception:
            if (attempts := attempts - 1) == 0:
                raise


def main() -> None:
    with open('jmcomic-link.txt') as f:
        link_domain = f.read().partition('||')[0]

    res = CLIENT.get(f'https://{link_domain}/')
    if True:
        while (res := get_domain(link_domain)).is_redirect:
            link_domain = extract_location(res)
        if res.is_success:
            write_result('jmcomic-link.txt', f'{link_domain}||g', f'JM-link(g) {link_domain}')
        else:
            assert (proxy := getenv('JM_PROXY'))
            assert (path := getenv('JM_PROXY_PATH'))
            while (res := retry_get(f'https://{proxy}/{path}/{link_domain}/')).is_redirect:
                link_domain = URL(res.headers['Location']).host
            if res.is_success:
                write_result('jmcomic-link.txt', f'{link_domain}||p', f'JM-link(p) {link_domain}')
            else:
                raise Exception(f'HTTP {res.status_code}')

    BEGIN = '<h1>禁漫天堂發布頁</h1>'
    END = 'APP軟件下載'
    text = (text := res.text)[(index := text.index(BEGIN)) : text.index(END, index)]
    text = text.replace('&nbsp;', ' ')
    text = re.sub(r'<.+?>', ' ', text)
    domains = re.findall(r'[-\w]+\.[-\w.]+', text)
    # TODO: possible redirection
    COUNT = len(PREFIX := ['18comic.vip', '18comic.ink', 'jmcomic-zzz.one', 'jmcomic-zzz.org'])
    assert domains[:COUNT] == PREFIX
    assert len(domains) > COUNT
    result = ','.join(domains := list(map(str.lower, domains[COUNT:])))

    write_result('jmcomic.txt', result, f'JM {result}')
