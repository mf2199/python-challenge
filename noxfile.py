# -*- coding: utf-8 -*-

# from __future__ import absolute_import

import os

import nox

DEFAULT_PYTHON_VERSION = "3.8"
UNIT_TEST_PYTHON_VERSIONS = ["3.8"]


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
