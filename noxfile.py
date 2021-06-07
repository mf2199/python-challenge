# -*- coding: utf-8 -*-

import os

import nox

DEFAULT_PYTHON_VERSION = "3.8"
UNIT_TEST_PYTHON_VERSIONS = ["3.8"]

BLACK_VERSION = "black==19.10b0"
BLACK_PATHS = ["service", "tests", "handler.py", "noxfile.py"]


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION)
    session.run(
        "black", "--check", *BLACK_PATHS, "--line-length", "79",
    )
    session.run("flake8", "handler.py", "service", "tests")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black.

    Format code to uniform standard.
    """
    session.install(BLACK_VERSION)
    session.run(
        "black", *BLACK_PATHS, "--line-length", "79",
    )


def default(session):
    session.install("faker", "mock", "pytest", "pytest-cov")

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        "--cov=tests",
        "--cov-append",
        # "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "test_models.py"),
        # "tests",
        *session.posargs,
    )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    """Run the unit test suite."""
    default(session)
