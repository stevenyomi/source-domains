def http_get(url: str, *, headers=None):
    from httpx import get

    if (res := get(url, headers=headers)).status_code != 200:
        raise Exception(f"HTTP {res.status_code}")
    return res


def write_result(filename: str, content: str, commit_message: str) -> None:
    with open(filename, "w") as f:
        f.write(content)

    with open(".git/COMMIT_EDITMSG", "w") as f:
        f.write(commit_message)
