import pytest
from demorepo import commands


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


def mock_subprocess_run(*args, **kwargs):
    mock_dict["mock_subprocess_run"] += 1
    class MockReturn:
        def __init__(self):
            self.stdout = b''
            self.stderr = b''
            self.returncode = 0
    return MockReturn()

@pytest.fixture
def setup_run_init(monkeypatch):
    args = {
        'command': 'init',
        'ci_tool': 'gitlab',
        'path': 'tests/projects',
        'recursive_deps': False
    }
    # Master branch: all the projects
    monkeypatch.setenv('CI_COMMIT_REF_NAME', 'master')
    commands.init(args)

