def http_get(url: str, *, headers=None):
    from httpx import get

    if (res := get(url, headers=headers)).status_code != 200:
        raise Exception(f"HTTP {res.status_code}")
    return res


def http_retry_get(url: str):
    from httpx import Client
    from tenacity import retry, stop_after_attempt

    @retry(stop=stop_after_attempt(3))
    def make_request(client: Client, url: str):
        res = client.get(url)
        if res.status_code >= 500:
            raise Exception(f"HTTP {res.status_code}")
        return res

    with Client() as client:
        res = make_request(client, url)

    if res.status_code != 200:
        raise Exception(f"HTTP {res.status_code}")
    return res


def write_result(filename: str, content: str, commit_message: str) -> None:
    with open(filename, "w") as f:
        f.write(content)

    with open(".git/COMMIT_EDITMSG", "w") as f:
        f.write(commit_message)
