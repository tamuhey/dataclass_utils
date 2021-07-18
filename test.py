import asyncio
from typing import Union
from typing_extensions import Literal, TypeGuard, get_args
import itertools
import subprocess


T_PYTHON_VERSIONS = Literal["3.7", "3.8", "3.9", "3.10-rc"]
PYTHON_VERSIONS = set(get_args(T_PYTHON_VERSIONS))


def main(python_version: str, no_build: bool = False):
    if is_python_version(python_version):
        asyncio.run(run(python_version, no_build))
    elif python_version == "all":
        tasks = [run(v, no_build) for v in PYTHON_VERSIONS]
        asyncio.run(asyncio.gather(*tasks))
    else:
        print(type(python_version))
        raise ValueError(f"Invalid python_version argument: {python_version}")


def is_python_version(version: str) -> TypeGuard[T_PYTHON_VERSIONS]:
    return version in PYTHON_VERSIONS


async def run(python_version: T_PYTHON_VERSIONS, no_build: bool):
    tag = f"dataclass_utils_{python_version}"
    if not no_build:
        cmd = f"docker build -t {tag} --build-arg PYTHON_VERSION={python_version} ."
        print("Build")
        print(cmd)
        proc = await asyncio.create_subprocess_shell(cmd)
        ret = await proc.wait()
        print(ret)
    test_cmd = f"docker run -it --rm {tag} make test"
    proc = await asyncio.create_subprocess_shell(test_cmd)
    ret = await proc.wait()
    print(ret)


if __name__ == "__main__":
    parser = Argument
    fire.Fire(main)
