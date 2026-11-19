import json
import re

from common import http_get, write_result


def main() -> None:
    res = http_get('https://wnacglink.com/')
    assert (config := re.search(r'window\.__INITIAL_CONFIG__=(\{.+?\});</script>', res.text, re.S))

    urls, domains = [], []
    for site in json.loads(config.group(1))["sites"]:
        urls.append(site['url'])
        domains.append(site['url'].removeprefix('https://www.'))

    assert len(urls) > 0

    write_result('wnacg.txt', ','.join(urls), 'WNACG ' + ','.join(domains))
