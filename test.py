import asyncio
from pathlib import Path
from asyncio.subprocess import PIPE, Process
import logging
import pystructopt
from dataclasses import dataclass, field
from typing import Union
from typing_extensions import Literal, TypeGuard, get_args
import logging

logger = logging.getLogger(__name__)


T_PYTHON_VERSIONS = Literal["3.7", "3.8", "3.9", "3.10-rc"]
PYTHON_VERSIONS = set(get_args(T_PYTHON_VERSIONS))


@dataclass
class Opts:
    python_version: Union[T_PYTHON_VERSIONS, Literal["all"]] = field(
        metadata={"positional": True}
    )
    no_build: bool = False


async def main():
    opts = pystructopt.parse(Opts)
    if is_python_version(opts.python_version):
        await run(opts.python_version, opts.no_build)
    elif opts.python_version == "all":
        tasks = [run(v, opts.no_build) for v in PYTHON_VERSIONS]
        await asyncio.gather(*tasks)
    else:
        raise ValueError(f"Invalid python_version argument: {opts.python_version}")


def is_python_version(version: str) -> TypeGuard[T_PYTHON_VERSIONS]:
    return version in PYTHON_VERSIONS


async def run(python_version: T_PYTHON_VERSIONS, no_build: bool):
    mod = Path(__file__).parent.absolute().parts[-1]
    tag = f"{mod}_{python_version}"
    if not no_build:
        cmd = f"docker build -t {tag} --build-arg PYTHON_VERSION={python_version} ."
        logger.info("Build")
        logger.info(cmd)
        proc = await asyncio.create_subprocess_exec(*cmd.split())
        if await proc.wait() != 0:
            raise ValueError(cmd)

    test_cmd = f"docker run --rm {tag} make test"
    proc = await asyncio.create_subprocess_exec(*test_cmd.split())
    if await proc.wait() != 0:
        raise ValueError(test_cmd)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
