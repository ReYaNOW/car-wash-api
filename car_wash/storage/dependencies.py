from fastapi import File, HTTPException, UploadFile

MAX_FILE_SIZE = 30 * 1024 * 1024  # 30 Mb


async def validate_img(
    image: UploadFile | str | None = File(None),
) -> UploadFile | None:
    if not image:
        return None

    if not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=415,
            detail='Only images are allowed',
        )

    if image.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail='File too large')
    return image
