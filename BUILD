load("@pip//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary", "py_test")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")

# pip update
compile_pip_requirements(
    name = "requirements",
    extra_args = ["--allow-unsafe"],
    requirements_in = "requirements.txt",
    requirements_txt = "requirements_lock.txt",
)

# test
py_test(
    name = "test",
    srcs = glob([
        "dataclass_utils/**/*.py",
        "tests/**/*.py",
        "test.py",
    ]),
    deps = [
        requirement("pytest"),
        requirement("typing_extensions"),
    ],
)
