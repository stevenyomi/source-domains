import re

from common import http_get, write_result

def main() -> None:
    res = http_get('https://wnacg.date/')
    regex = re.compile(r'<a href="(https?://([.\w]+))/?" target="_blank"><i>\2</i></a>')

    urls, domains = [], []
    for match in regex.finditer(res.text):
        urls.append(match.group(1))
        domains.append(match.group(2).removeprefix('www.'))

    assert len(urls) > 0

    write_result('wnacg.txt', ','.join(urls), 'WNACG ' + ','.join(domains))


main()
