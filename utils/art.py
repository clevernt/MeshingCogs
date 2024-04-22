import re

# TODO


def get_mentions(message):
    return re.findall(r"@(\w+)", message)
