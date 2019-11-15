from invoke import task

from ..config import *

import sys

@task
def dev(ctx):
    """Recreate from scratch the wepy development environment."""

    ctx.run(f"conda create -y -n {PY_ENV_NAME} python={PY_VERSION}",
        pty=True)

    # install package
    #ctx.run(f"$ANACONDA_DIR/envs/{PY_ENV_NAME}/bin/pip install -e .")

    # install the dev dependencies
    #ctx.run(f"$ANACONDA_DIR/envs/{PY_ENV_NAME}/bin/pip install -r requirements_dev.txt")