#!/usr/bin/env python3

# Package.py
# Created by Charles Pisciotta
# September 15, 2021

# This data model was automatically created using quicktype
# https://app.quicktype.io/

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class License:
    key: str
    name: str
    spdx_id: str
    url: str
    node_id: str
    html_url: Optional[str] = None


@dataclass
class Owner:
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool


@dataclass
class Permissions:
    pull: bool
    push: bool
    admin: bool


@dataclass
class Parent:
    id: int
    node_id: str
    name: str
    full_name: str
    owner: Owner
    private: bool
    html_url: str
    description: str
    fork: bool
    url: str
    archive_url: str
    assignees_url: str
    blobs_url: str
    branches_url: str
    collaborators_url: str
    comments_url: str
    commits_url: str
    compare_url: str
    contents_url: str
    contributors_url: str
    deployments_url: str
    downloads_url: str
    events_url: str
    forks_url: str
    git_commits_url: str
    git_refs_url: str
    git_tags_url: str
    git_url: str
    issue_comment_url: str
    issue_events_url: str
    issues_url: str
    keys_url: str
    labels_url: str
    languages_url: str
    merges_url: str
    milestones_url: str
    notifications_url: str
    pulls_url: str
    releases_url: str
    ssh_url: str
    stargazers_url: str
    statuses_url: str
    subscribers_url: str
    subscription_url: str
    tags_url: str
    teams_url: str
    trees_url: str
    clone_url: str
    mirror_url: str
    hooks_url: str
    svn_url: str
    homepage: str
    language: None
    forks_count: int
    stargazers_count: int
    watchers_count: int
    size: int
    default_branch: str
    open_issues_count: int
    is_template: bool
    topics: List[str]
    has_issues: bool
    has_projects: bool
    has_wiki: bool
    has_pages: bool
    has_downloads: bool
    archived: bool
    disabled: bool
    visibility: str
    pushed_at: datetime
    created_at: datetime
    updated_at: datetime
    permissions: Permissions
    allow_rebase_merge: bool
    temp_clone_token: str
    allow_squash_merge: bool
    allow_auto_merge: bool
    delete_branch_on_merge: bool
    allow_merge_commit: bool
    subscribers_count: int
    network_count: int
    license: License
    forks: int
    open_issues: int
    watchers: int


@dataclass
class Package:
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: Owner
    html_url: str
    description: str
    fork: bool
    url: str
    forks_url: str
    keys_url: str
    collaborators_url: str
    teams_url: str
    hooks_url: str
    issue_events_url: str
    events_url: str
    assignees_url: str
    branches_url: str
    tags_url: str
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: str
    stargazers_url: str
    contributors_url: str
    subscribers_url: str
    subscription_url: str
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: str
    archive_url: str
    downloads_url: str
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: str
    created_at: datetime
    updated_at: datetime
    pushed_at: datetime
    git_url: str
    ssh_url: str
    clone_url: str
    svn_url: str
    homepage: str
    size: int
    stargazers_count: int
    watchers_count: int
    language: None
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    forks_count: int
    archived: bool
    disabled: bool
    open_issues_count: int
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    network_count: int
    subscribers_count: int
    mirror_url: Optional[str] = None
    license: Optional[License] = None
    allow_forking: Optional[bool] = None
    temp_clone_token: Optional[str] = None
    is_template: Optional[bool] = None
    topics: Optional[List[str]] = None
    visibility: Optional[str] = None
    permissions: Optional[Permissions] = None
    allow_rebase_merge: Optional[bool] = None
    template_repository: Optional[Parent] = None
    allow_squash_merge: Optional[bool] = None
    allow_auto_merge: Optional[bool] = None
    delete_branch_on_merge: Optional[bool] = None
    allow_merge_commit: Optional[bool] = None
    organization: Optional[Owner] = None
    parent: Optional[Parent] = None
    source: Optional[Parent] = None
    #message: Optional[str] = None
    #documentation_url: Optional[str] = None