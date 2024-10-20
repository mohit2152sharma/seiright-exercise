import logging
import os
from functools import wraps
from time import time
from typing import Any, Optional

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
