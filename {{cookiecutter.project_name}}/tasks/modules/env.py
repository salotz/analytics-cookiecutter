from invoke import task

from ..config import *

from . import org as org_tasks

import sys

@task(pre=[org_tasks.tangle])
def common(cx):
    """Recreate from scratch the wepy development environment."""

    env_subname = 'common'

    cx.run(f"conda create -y -n {PY_ENV_NAME} python={PY_VERSION}",
        pty=True)

    # install the local package
    cx.run(f"$ANACONDA_DIR/envs/{PY_ENV_NAME}/bin/pip install -e .")

    # install the pip dev dependencies
    cx.run(f"$ANACONDA_DIR/envs/{PY_ENV_NAME}/bin/pip install -r configs/requirements.txt")

    # install the conda dev dependencies
    cx.run(f"conda env update -n {PY_ENV_NAME} --file configs/{env_subname}.env.yaml")

    print("--------------------------------------------------------------------------------")
    print(f"run: conda activate {PY_ENV_NAME}")
