import re

regex = r"https?://(?:twitter|X|vxtwitter|fxtwitter)\.com/[A-Za-z0-9_]+/status/(\d+)"


def find_tweet(message: str) -> re.Match[str] | None:
    match = re.search(pattern=regex, string=message, flags=re.IGNORECASE)
    return match if match else None


def get_tweet_id(message: str) -> str | None:
    match = find_tweet(message)
    if match:
        return match.group(1)
    return None


def get_tweet_link(message: str) -> str | None:
    match = find_tweet(message)
    if match:
        return match.group(0)
    return None
