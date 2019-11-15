from setuptools import setup, find_packages

setup(name='{{cookiecutter.project_name}}',
      version="0.1",
      packages=['{{cookiecutter.project_slug}}'],
      package_dir={'' : 'src'},
      package_data={},
      entry_points={
          'console_scripts' : [
          ]}
)
