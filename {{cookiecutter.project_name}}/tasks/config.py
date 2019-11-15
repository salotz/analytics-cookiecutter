"""User settings for a project."""

# load the system configuration. You can override them in this module,
# but beware it might break stuff
from .sysconfig import *

# import plugins:

from .plugins import custom

# specify which plugins to install, the custom one is included by
# default to get users going
PLUGIN_MODULES = [custom, ]

### Project Metadata

# the name of the project
PROJECT_NAME = "{{ cookiecutter.project_name }}"

# the url compatible name of the project
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"

# copyright options:
# https://en.wikipedia.org/wiki/Creative_Commons_license#Seven_regularly_used_licenses
# CCO, BY, BY-SA, BY-NC, BY-NC-SA, BY-ND, BY-NC-ND

# copyright of the project
PROJECT_COPYRIGHT = "{{ cookiecutter.copyright }}"

## Project Owner

# real name of the owner of the project
OWNER_NAME = "{{ cookiecutter.owner_name}}"

# email of the owner
OWNER_EMAIL = "{{ cookiecutter.owner_email }}"

# handle/username/nickname of the owner
OWNER_NICKNAME = "{{ cookiecutter.owner_nickname }}"

## Environment information

# which shell profile to use
SHELL_PROFILE = "{{ cookiecutter.shell_profile }}"

# the subdomain of tree this project is in
REFUGUE_DOMAIN = '{{ cookiecutter.refugue_domain }}'

## Updating

# where to download git repos to; the "cookiejar"
COOKIEJAR_DIR = "$HOME/tmp/cookiejar"

# URL to get updates from
UPDATE_URL="https://github.com/salotz/analytics-cookiecutter.git"

### Project Configuration

# directory that the project is actually living in
PROJECT_DIR = "{{ cookiecutter.project_dir }}"

# directories which will be assumed to exist, these will be built with
# the "init" command
PROJECT_DIRS = [
    'src',
    'scripts',
    'data',
    'cache',
    'db',
    'tmp',
    'scratch',
    'troubleshoot',
]


### Environments

PY_ENV_NAME = '{{ cookiecutter.project_name }}-project'
PY_VERSION = '{{ cookiecutter.py_version }}'

### VCS

## Git

# specify the directories which should be stored in git-lfs
GIT_LFS_TARGETS = []


### Packaging

## Python


### Resources

# Project resources are things that get managed outside of the actual
# directory tree that it sits in
RESOURCE_DIR = {% if cookiecutter.refugue_domain is ne ':none' %}"$TREE/{{cookiecutter.refugue_domain}}/resources/project-resources/{{cookiecutter.project_name}}"{% else %}None{% endif %}

RESOURCES = [
    'cache',
    'data',
    'db',
]

