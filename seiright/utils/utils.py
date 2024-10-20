import hashlib
import logging
import os
from functools import wraps
from time import time
from typing import Any, Optional

import boto3

logger = logging.getLogger(__name__)


def get_env_var(
    var_name: str,
    default: Any = None,
    raise_error: bool = True,
    error_msg: Optional[str] = None,
) -> Any:
    _r = os.getenv(var_name, default)
    if _r is None:
        if raise_error:
            if error_msg:
                raise KeyError(error_msg)
            else:
                raise KeyError(f"Environment variable {var_name} not found")
    return _r


def timer(f):

    @wraps(f)
    def _wrap(*args, **kwargs):
        t0 = time()
        result = f(*args, **kwargs)
        t1 = time()
        logger.info(f"Function {f.__name__!r} executed in {(t1-t0):.4f}s")
        return result

    return _wrap


def cache(func):
    @wraps(func)
    def _wrap(*args, **kwargs):
        args_hash = hashlib.sha1(
            str(args).encode("utf-8") + str(kwargs).encode("utf-8")
        ).hexdigest()
        cache_key = f"CACHE_{func.__name__}_{args_hash}"
        value = os.getenv(cache_key)
        if value:
            return value
        value = func(*args, **kwargs)
        os.environ[cache_key] = value
        return value

    return _wrap


@cache
def secret(secret_string: str, region_name: str = "ap-south-1") -> str:
    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_string)
    secret = response["SecretString"]
    return secret
