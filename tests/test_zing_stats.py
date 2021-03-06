#!/usr/bin/env python2
#
# (c) Copyright 2017 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import zing_stats


def test_helloworld():
        assert 1 == 1


def test_parse_gerrit_change_message():
    messages = [
        {
            '_revision_number': 1,
            'author': {
                '_account_id': 12
            },
            'date': '2017-04-20 17:15:24.000000000',
            'id': '9a5c5d37_e7c9a25b',
            'message': 'Uploaded patch set 1.'
        },
        {
            '_revision_number': 1,
            'author': {
                '_account_id': 6
            },
            'date': '2017-04-20 17:15:35.000000000',
            'id': '9a5c5d37_a7c3aa37',
            'message': 'Patch Set 1:\n\nStarting check jobs.'
        },
        {
            '_revision_number': 1,
            'author': {
                '_account_id': 6
            },
            'date': '2017-04-20 17:15:44.000000000',
            'id': '9a5c5d37_67ddb214',
            'message': 'Patch Set 1: Verified+1\n\nBuild succeeded\n\n- https://zing.example.net/jenkins/job/test-check/6/ : SUCCESS in 7s'  # noqa
        },
    ]
    msg0 = zing_stats.parse_ci_job_comments(messages[0])
    assert msg0 == {}
    msg1 = zing_stats.parse_ci_job_comments(messages[1])
    assert msg1 == {}
    msg2 = zing_stats.parse_ci_job_comments(messages[2])
    assert msg2['num'] == '1'
    assert msg2['status'] == 'succeeded'
    assert msg2['v_score'] == '+1'

    assert len(msg2['jobs']) == 1
    assert msg2['jobs'][0]['name'] == 'test-check'
    assert msg2['jobs'][0]['non_voting'] is None


def test_parse_github_change_message():
    messages = [
        {
            "body": "@aaaa @bbbb @ccccc xxxxxxxx",
            "created_at": "2017-12-06T10:49:06Z",
            "html_url": "https://github.example.com/foo/api/pull/1153#issuecomment-429779",
            "id": 429779,
            "issue_url": "https://github.example.com/api/v3/repos/foo/api/issues/1153",
            "updated_at": "2017-12-06T10:49:06Z",
            "url": "https://github.example.com/api/v3/repos/foo/api/issues/comments/429779",
            "user": {
                "avatar_url": "https://avatars.github.example.com/u/19638?",
                "events_url": "https://github.example.com/api/v3/users/a_user/events{/privacy}",
                "followers_url": "https://github.example.com/api/v3/users/a_user/followers",
                "following_url": "https://github.example.com/api/v3/users/a_user/following{/other_user}",
                "gists_url": "https://github.example.com/api/v3/users/a_user/gists{/gist_id}",
                "gravatar_id": "",
                "html_url": "https://github.example.com/a_user",
                "id": 19638,
                "login": "a_user",
                "organizations_url": "https://github.example.com/api/v3/users/a_user/orgs",
                "received_events_url": "https://github.example.com/api/v3/users/a_user/received_events",
                "repos_url": "https://github.example.com/api/v3/users/a_user/repos",
                "site_admin": "false",
                "starred_url": "https://github.example.com/api/v3/users/a_user/starred{/owner}{/repo}",
                "subscriptions_url": "https://github.example.com/api/v3/users/a_user/subscriptions",
                "type": "User",
                "url": "https://github.example.com/api/v3/users/a_user"
            }
        },
        {
            "body": "Build succeeded\n\n- http://logs.example.net/check-github/foo/api/111153/151255557209.72/foo-example-check : SUCCESS in 2m 38s\n- http://logs.example.net/check-github/foo/api/111153/151112557209.72/foo-sec-scan : SUCCESS in 4s (non-voting)\n- http://logs.example.net/check-github/foo/api/122153/151332557209.72/another-scan : SUCCESS in 4s (non-voting)\n",
            "created_at": "2017-12-06T10:49:06Z",
            "html_url": "https://github.example.com/foo/api/pull/1153#issuecomment-429779",
            "id": 429779,
            "issue_url": "https://github.example.com/api/v3/repos/foo/api/issues/1153",
            "updated_at": "2017-12-06T10:49:06Z",
            "url": "https://github.example.com/api/v3/repos/foo/api/issues/comments/429779",
            "user": {
                "avatar_url": "https://avatars.github.example.com/u/19638?",
                "events_url": "https://github.example.com/api/v3/users/a_user/events{/privacy}",
                "followers_url": "https://github.example.com/api/v3/users/a_user/followers",
                "following_url": "https://github.example.com/api/v3/users/a_user/following{/other_user}",
                "gists_url": "https://github.example.com/api/v3/users/a_user/gists{/gist_id}",
                "gravatar_id": "",
                "html_url": "https://github.example.com/a_user",
                "id": 19638,
                "login": "a_user",
                "organizations_url": "https://github.example.com/api/v3/users/a_user/orgs",
                "received_events_url": "https://github.example.com/api/v3/users/a_user/received_events",
                "repos_url": "https://github.example.com/api/v3/users/a_user/repos",
                "site_admin": "false",
                "starred_url": "https://github.example.com/api/v3/users/a_user/starred{/owner}{/repo}",
                "subscriptions_url": "https://github.example.com/api/v3/users/a_user/subscriptions",
                "type": "User",
                "url": "https://github.example.com/api/v3/users/a_user"
            }
        },
    ]
    msg0 = zing_stats.parse_pr_message(messages[0])
    assert msg0 == {}
    msg1 = zing_stats.parse_pr_message(messages[1])
    assert msg1['num'] == None
    assert msg1['status'] == 'succeeded'
    assert msg1['v_score'] == None
    assert len(msg1['jobs']) == 3
    assert msg1['jobs'][0]['name'] == 'foo-example-check'
    assert msg1['jobs'][0]['non_voting'] is None
    assert msg1['jobs'][1]['name'] == 'foo-sec-scan'
    assert msg1['jobs'][1]['non_voting'] == ' (non-voting)'
    assert msg1['jobs'][2]['name'] == 'another-scan'
    assert msg1['jobs'][2]['non_voting'] == ' (non-voting)'
