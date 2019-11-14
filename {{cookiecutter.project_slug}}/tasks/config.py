"""Default settings for a project."""

# import plugins:

# specify which plugins to install
PLUGIN_MODULES = []

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


### Project Configuration

# directory that the project is actually living in
PROJECT_DIR = f"$TREE/{REFUGUE_DOMAIN}/projects/{PROJECT_SLUG}"

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

PY_ENV_NAME = '{{ cookiecutter.project_slug }}-project'
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
RESOURCE_DIR = f"$TREE/{REFUGUE_DOMAIN}/resources/project-resources/{PROJECT_NAME}"

RESOURCES = [
    'cache',
    'data',
    'db',
]

