import git
import requests
import os

import demorepo.config
from . import MockGitRepo, setup
from demorepo.commands.ci import get_lgc, get_diff

config_plain = {
    "projects": {
        "target_A": {},
        "target_B": {},
        "target_C": {}
    }
}


def test_get_diff(monkeypatch):
    paths = dict(target_A="projects/target_A")

    monkeypatch.setattr(git, 'Repo', MockGitRepo)

    diffs = get_diff(paths, "sha!")
    assert diffs == []


def test_get_lgc(setup):
    def mock_get(*args, **kwargs):
        response = [
            {
                "sha": '85ad21771ffab14ac3a5f0347c00e28a9bb45cc1'
            }
        ]

        class Get:
            def json(self):
                return response
        return Get()
    setup.setattr(requests, 'get', mock_get)
    setup.setattr(git, 'Repo', MockGitRepo)

    setup.setenv('CI_COMMIT_REF_NAME', 'develop')
    setup.setenv('GITLAB_API_KEY', '1234')
    setup.setenv('CI_PROJECT_ID', '1234')

    sha = get_lgc("gitlab", None)

    assert sha == "85ad21771ffab14ac3a5f0347c00e28a9bb45cc1"
