from invoke import task

import sys
import os
import os.path as osp
from pathlib import Path

from ..config import *

from . import org as org_tasks

ENV_METHOD = 'conda'

ENVS_DIR = 'configs/envs'

# directories the actual environments are stored
VENV_DIR = "_venv"
CONDA_ENVS_DIR = "_conda_envs"

SELF_REQUIREMENTS = 'self.requirements.txt'
PYTHON_VERSION_FILE = 'py_version.txt'
DEV_REQUIREMENTS_LIST = 'dev.requirements.list'

DEFAULT_ENV = 'common_dev'


def parse_list_format(list_str):

    return [line for line in list_str.split('\n')
            if not line.startswith("#") and line.strip()]

@task
def deps_pip_pin(cx, name=DEFAULT_ENV, upgrade=False):

    path = Path(ENVS_DIR) / name

    # gather any development repos that are colocated on this machine
    # and solve the dependencies together

    # to get the development repos read the DEV list
    with open(path / DEV_REQUIREMENTS_LIST) as rf:
        dev_repo_specs = parse_list_format(rf.read())

    # for each repo spec add this to the list of specs to evaluate for
    specs = []
    for dev_repo_spec in dev_repo_specs:
        assert osp.exists(dev_repo_spec), f"Repo spec {dev_repo_spec} doesn't exist"

        specs.append(dev_repo_spec)


    spec_str = f"{path}/requirements.in " + " ".join(specs)

    print(spec_str)

    upgrade_str = ''
    if upgrade:
        upgrade_str = "--upgrade"

    cx.run("pip-compile "
           f"{upgrade_str} "
           f"--output-file={path}/requirements.txt "
           f"{spec_str}")

    # SNIPPET: generate hashes is not working right, or just confusing me
    # cx.run("python -m piptools compile "
    #        "--generate-hashes "
    #        "--output-file=requirements.txt "
    #        f"requirements.in")

# @task
# def deps_pip_upgrade(cx, name=DEFAULT_ENV):

#     path = Path(ENVS_DIR) / name

#     cx.run("python -m piptools compile "
#            "--upgrade "
#            f"--output-file={path}/requirements.txt "
#            f"{path}/requirements.in")

## conda: managing conda dependencies

@task
def deps_conda_pin(cx, name=DEFAULT_ENV, upgrade=False):

    # STUB: currently upgrade does nothing

    env_spec_path = Path(ENVS_DIR) / name

    assert osp.exists(env_spec_path / 'env.yaml'), \
        "There must be an 'env.yaml' file to compile from"

    # delete the pinned file
    if osp.exists(env_spec_path / 'env.pinned.yaml'):
        os.remove(env_spec_path / 'env.pinned.yaml')

    # make the environment under a mangled name so we don't screw with
    # the other one
    mangled_name = f"__mangled_{name}"
    env_dir = conda_env(cx, name=mangled_name)

    # REFACT: This is copied from the conda_env function and should be
    # factored into it's own thing

    # then install the packages so we can export them
    with cx.prefix(f'eval "$(conda shell.bash hook)" && conda activate {env_dir}'):

        # only install the declared dependencies
        cx.run(f"conda env update "
               f"--prefix {env_dir} "
               f"--file {env_spec_path}/env.yaml")

    # pin to a 'env.pinned.yaml' file
    cx.run(f"conda env export "
           f"-p {env_dir} "
           f"-f {env_spec_path}/env.pinned.yaml")


    # then destroy the temporary mangled env
    cx.run(f"rm -rf {env_dir}")

# altogether
@task
def deps_pin(cx, name=DEFAULT_ENV, upgrade=False):

    deps_pip_pin(cx, name=name, upgrade=upgrade)
    deps_conda_pin(cx, name=name, upgrade=upgrade)

    # SNIPPET, IDEA: automatic git commits could be supported but
    # pairs poorly with the rest being automatic, would need better
    # semantics about splitting them up so they are analyzable, and no
    # such tool is planned so the consistency of commit messages is
    # unwarranted as of yet
    #
    # cx.run(f"git add -A && git commit -m 'pinned dependencies for the env: {name}'")

## Making environments

def conda_env(cx, name=DEFAULT_ENV):

    # locally scoped since the environment is global to the
    # anaconda installation
    env_name = name

    # where the specs of the environment are
    env_spec_path = Path(ENVS_DIR) / name

    # using the local envs dir
    env_dir = Path(CONDA_ENVS_DIR) / name

    # figure out which python version to use, if the 'pyversion.txt'
    # file exists read it
    py_version_path = env_spec_path / PYTHON_VERSION_FILE
    if osp.exists(py_version_path):
        with open(py_version_path, 'r') as rf:
            py_version = rf.read().strip()

        # TODO: validate the string for python version

    # otherwise use the one you are currently using
    else:
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    # create the environment
    cx.run(f"conda create -y "
           f"--prefix {env_dir} "
           f"python={py_version}",
        pty=True)

    with cx.prefix(f'eval "$(conda shell.bash hook)" && conda activate {env_dir}'):

        # install the conda dependencies. choose a specification file
        # based on these priorities of most pinned to least frozen.
        if osp.exists(env_spec_path / "env.pinned.yaml"):

            cx.run(f"conda env update "
                   f"--prefix {env_dir} "
                   f"--file {env_spec_path}/env.pinned.yaml")


        elif osp.exists(env_spec_path / "env.yaml"):

            cx.run(f"conda env update "
                   f"--prefix {env_dir} "
                   f"--file {env_spec_path}/env.yaml")

        else:
            # don't do a conda env pin
            pass


        # install the extra pip dependencies
        if osp.exists(f"{env_spec_path}/requirements.txt"):
            cx.run(f"{env_dir}/bin/pip install "
                   f"-r {env_spec_path}/requirements.txt")

        # install the package itself
        if osp.exists(f"{env_spec_path}/{SELF_REQUIREMENTS}"):
            cx.run(f"{env_dir}/bin/pip install -r {env_spec_path}/{SELF_REQUIREMENTS}")

    print("--------------------------------------------------------------------------------")
    print(f"run: conda activate {env_dir}")

    return env_dir


def venv_env(cx, name=DEFAULT_ENV):

    venv_dir_path = Path(VENV_DIR)
    venv_path = venv_dir_path / name

    env_spec_path = Path(ENVS_DIR) / name

    # ensure the directory
    cx.run(f"mkdir -p {venv_dir_path}")

    # create the env requested
    cx.run(f"python -m venv {venv_path}")

    # then install the things we need
    with cx.prefix(f"source {venv_path}/bin/activate"):

        if osp.exists(f"{env_spec_path}/{SELF_REQUIREMENTS}"):
            cx.run(f"pip install -r {env_spec_path}/requirements.txt")

        else:
            print("No requirements.txt found")

        # if there is a 'self.requirements.txt' file specifying how to
        # install the package that is being worked on install it
        if osp.exists(f"{env_spec_path}/{SELF_REQUIREMENTS}"):
            cx.run(f"pip install -r {env_spec_path}/{SELF_REQUIREMENTS}")

        else:
            print("No self.requirements.txt found")

    print("----------------------------------------")
    print("to activate run:")
    print(f"source {venv_path}/bin/activate")

@task(pre=[org_tasks.tangle], default=True)
def env(cx, name=DEFAULT_ENV):

    # choose your method:
    if ENV_METHOD == 'conda':
        conda_env(cx, name=name)

    elif ENV_METHOD == 'venv':
        venv_env(cx, name=name)

    else:
        print(f"method {ENV_METHOD} not recognized")
