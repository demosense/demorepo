from demorepo.commands import ci
import git
import requests
import os
from . import MockGitRepo, setup


def test_last_green_commit_master(setup):
    args = {
        'command': 'init',
        'ci_tool': 'gitlab',
        'path': 'tests/projects',
        'recursive_deps': False}

    set_all_projects = set()
    set_all_projects.add('p1')
    set_all_projects.add('p2')
    set_all_projects.add('p3')

    # Master branch: all the projects
    setup.setenv('CI_COMMIT_REF_NAME', 'master')
    targets = ci.get_targets(args)
    assert {t for t in targets} == set_all_projects

def test_last_green_commit_tag(setup):
    args = {
        'command': 'init',
        'ci_tool': 'gitlab',
        'path': 'tests/projects',
        'recursive_deps': False}

    set_all_projects = set()
    set_all_projects.add('p1')
    set_all_projects.add('p2')
    set_all_projects.add('p3')

    # Tag: all the projects
    setup.setenv('CI_COMMIT_TAG', '1.0')
    targets = ci.get_targets(args)
    assert {t for t in targets} == set_all_projects


def test_last_green_commit_release(setup):
    args = {
        'command': 'init',
        'ci_tool': 'gitlab',
        'path': 'tests/projects',
        'recursive_deps': False}

    set_all_projects = set()
    set_all_projects.add('p1')
    set_all_projects.add('p2')
    set_all_projects.add('p3')

    # Release branch: all the projects
    setup.setenv('CI_COMMIT_REF_NAME', 'release/1.0')
    targets = ci.get_targets(args)
    assert {t for t in targets} == set_all_projects


def test_last_green_commit_develop_recursive(setup):
    args = {
        'command': 'init',
        'ci_tool': 'gitlab',
        'path': 'tests/projects',
        'recursive_deps': True}

    set_projects = set()
    set_projects.add('p1')
    set_projects.add('p2')

    # Develop branch: mock the requests.get and the GitPython library
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
    MockGitRepo.DIFFS = [
        os.path.join(args['path'], 'must_be_filtered_file.txt'),
        os.path.join(args['path'], 'must_be_filtered_folder'),
        os.path.join(args['path'], 'p1/demorepo.yml')
    ]
    setup.setattr(git, 'Repo', MockGitRepo)

    setup.setenv('CI_COMMIT_REF_NAME', 'develop')
    setup.setenv('GITLAB_API_KEY', '1234')
    setup.setenv('CI_PROJECT_ID', '1234')

    targets = ci.get_targets(args)
    assert {t for t in targets} == set_projects
