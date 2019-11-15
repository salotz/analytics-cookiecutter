from invoke import task

PY_VERSION = "3.7"
PY_ENV_NAME = "analytics-cookiecutter-dev"
CLEAN_EXPRESSIONS = [
    "\"*~\"",
]


@task
def ls_clean(cx):

    for clean_expr in CLEAN_EXPRESSIONS:
        cx.run('find . -type f -name {} -print'.format(clean_expr))

@task(ls_clean)
def clean(cx):
    print("Deleting Targets")
    for clean_expr in CLEAN_EXPRESSIONS:
        cx.run('find . -type f -name {} -delete'.format(clean_expr))

@task
def env_dev(cx):
    """Recreate from scratch the wepy development environment."""

    cx.run(f"conda create -y -n {PY_ENV_NAME} python={PY_VERSION}",
        pty=True)

    cx.run(f"$ANACONDA_DIR/envs/{PY_ENV_NAME}/bin/pip install -r requirements.dev.txt")
