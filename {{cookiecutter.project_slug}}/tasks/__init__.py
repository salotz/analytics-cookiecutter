from invoke import Collection, task

# core modules for this project
from .modules import core
from .modules import py
from .modules import git
from .modules import meta
from .modules import project
from .modules import org
from .modules import env

# add all of the modules to the CLI
ns = Collection()


# first load all of the core objects
modules = [core, py, git, project, org, env,]

for module in modules:
    ns.add_collection(module)

# then the user defined stuff

try:
    # import all the user defined stuff and override
    from .config import plugin_modules as plugins

    for module in plugins:
        ns.add_collection(module)

except Exception as e:
    print("Loading plugins failed with error ignoreing:")
    print(e)
