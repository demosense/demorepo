import subprocess
import os
import pytest


class MockGit:
    def __init__(self, diff):
        self._diff = '\n'.join(diff)
        print(diff)

    def diff(self, *args, **kwarg):
        return self._diff


class MockGitRepo:
    DIFFS = []

    def __init__(self, path):
        self.path = path
        self.git = MockGit(MockGitRepo.DIFFS)

    def merge_base(self, *args):
        return args[0]  # Return the first argument (sha or commit reference)


mock_dict = {}


original_subprocess_run = subprocess.run


def mock_subprocess_run(*args, **kwargs):
    mock_dict["mock_subprocess_run"] += 1
    return original_subprocess_run(*args, **kwargs)


def mock_sys_exit(*args, **kwargs):
    mock_dict["mock_sys_exit"] += 1


@pytest.fixture()
def setup(monkeypatch):
    actual_path = os.getcwd()
    monkeypatch.setattr(os, 'getcwd', lambda: os.path.join(actual_path, 'tests'))
    yield monkeypatch