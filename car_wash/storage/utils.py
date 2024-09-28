import time

from pydantic import HttpUrl

MIN_ENOUGH_MINUTES = 5


def validate_link(url: HttpUrl, img_path: str) -> bool:
    folder_and_filename = url.path.rsplit('/')[-2:]
    path = '/'.join(folder_and_filename)

    if path != img_path:
        return False

    query_params = url.query_params()
    expires = None
    for k, v in query_params:
        if k == 'Expires':
            expires = v
            break

    if not expires:
        return False

    if not expires.isnumeric():
        return False
    expires = int(expires)

    current_time = int(time.time())
    time_left = expires - current_time

    if time_left < 0:
        return False
    _, remainder = divmod(time_left, 3600)
    minutes, _ = divmod(remainder, 60)

    return minutes < MIN_ENOUGH_MINUTES
