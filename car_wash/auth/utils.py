from passlib.context import CryptContext
from starlette.concurrency import run_in_threadpool

pwd_context = CryptContext(
    schemes=['argon2'],
    argon2__memory_cost=4096,
    argon2__parallelism=2,
    deprecated='auto',
)


async def verify_password_in_threadpool(plain_password, hashed_password):
    res = await run_in_threadpool(verify_pass, plain_password, hashed_password)
    return res


def verify_pass(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_pass_hash_in_threadpool(password):
    return await run_in_threadpool(get_pass_hash, password)


def get_pass_hash(password):
    return pwd_context.hash(password)
