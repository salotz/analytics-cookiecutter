from invoke import task

from ..config import *

@task()
def tangle(cx):

    # tangle them
    cx.run("emacs -Q --batch -l org project.org -f org-babel-tangle")

    # make them executable
    cx.run(f'chmod ug+x {PROJECT_DIR}/hpcc/scripts/*')

@task
def clean(cx):

    cx.run("rm -f scripts/*")
