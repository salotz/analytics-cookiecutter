from invoke import task

from ..config import *

@task()
def tangle(cx):
    """Tangle all the code blocks in project.org"""

    # tangle them
    cx.run("emacs -Q --batch -l org project.org -f org-babel-tangle")

    # make them executable
    cx.run(f'chmod ug+x {PROJECT_DIR}/scripts/*')

@task
def clean(cx):
    """Clean all the code that is tangled to:

    - scripts

    """

    cx.run("rm -f scripts/*")
