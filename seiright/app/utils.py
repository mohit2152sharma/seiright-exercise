import json
import os
import warnings
from pathlib import Path
from typing import Any, Dict


def get_env_var(
    env_var: str, default_value: Any = None, raise_error: bool = True
) -> str:
    """Fetches the variable from environment

    Args:
        env_var: environment variable to fetch
        default_value: default value of the environment variable if not present.
        raise_error: whether to raise error or warning if not present

    Raises:
        ValueError: Raises an error if `raise_error=True` and environment variable
        is not present in environment or the default value is `None`

    Returns:
        environment variable value
    """
    value = os.getenv(env_var, default_value)

    if value is None:
        msg = (
            f"Environment variable {env_var} is required but not present in environment"
        )
        if raise_error:
            raise ValueError(msg)
        else:
            warnings.warn(msg)

    return value


def read_db(file_name: str = "db.json") -> Dict[str, str]:
    """reads data from database (for this exercise, the  database is assumed to be a key/value store in a json file)

    Args:
        file_name: name of the json file

    Returns:
        A dictionary of data
    """
    file_path = Path(__file__).parent
    path = os.path.join(file_path, file_name)
    with open(path, "r") as file:
        data = json.loads(file.read())
    return data
