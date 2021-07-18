from typing import Union
from typing_extensions import Literal, TypeGuard, get_args
import fire
import multiprocessing
import itertools
import subprocess


T_PYTHON_VERSIONS = Literal["3.7", "3.8", "3.9", "3.10-rc"]
PYTHON_VERSIONS = set(get_args(T_PYTHON_VERSIONS))


def main(
    python_version: Union[T_PYTHON_VERSIONS, Literal["all"]], no_build: bool = False
):
    if is_python_version(python_version):
        run(python_version, no_build)
    elif python_version == "all":
        with multiprocessing.Pool(len(PYTHON_VERSIONS)) as p:
            args = zip(PYTHON_VERSIONS, itertools.repeat(no_build))
            result = p.starmap(run, args)
        print(result)


def is_python_version(version: str) -> TypeGuard[T_PYTHON_VERSIONS]:
    return version in PYTHON_VERSIONS


def run(python_version: T_PYTHON_VERSIONS, no_build: bool):
    tag = f"dataclass_utils_{python_version}"
    if not no_build:
        cmd = f"docker build -t {tag} --build-arg PYTHON_VERSION={python_version} ."
        print("Build")
        print(cmd)
        subprocess.run(cmd.split(), check=True)
    print("Test")
    test_cmd = f"docker run -it --rm {tag} make test"
    subprocess.run(test_cmd.split(), check=True)


if __name__ == "__main__":
    fire.Fire(main)
