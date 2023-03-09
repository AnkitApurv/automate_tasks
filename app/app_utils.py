from typing import Any, Dict

import yaml


def read_config(file_path: str) -> Dict[Any, Any]:
    with open(file=file_path, mode="rt", encoding="utf-8") as f:
        config: Dict[Any, Any] = yaml.safe_load(stream=f.read())
    return config


def write_config(file_path: str, config: Dict[Any, Any]) -> None:
    with open(file=file_path, mode="wt", encoding="utf-8") as f:
        yaml.safe_dump(data=config, stream=f)
    return
