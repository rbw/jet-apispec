# -*- coding: utf-8 -*-

import sys
import re
import pathlib
import subprocess
from shutil import rmtree

from setuptools import find_packages, setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.upload import upload

__requires__ = ['pipenv']

base_dir = pathlib.Path(__file__).parent


def parse_file(file_path):
    with open(base_dir / file_path, encoding='utf-8') as f:
        return f.read().strip()


def find_version(path):
    contents = parse_file(path)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", contents, re.M)
    if version_match:
        return version_match.group(1)

    raise RuntimeError('Unable to find version string.')


readme = parse_file('README.md')
version = find_version('jet_apispec/__init__.py')

pipenv_command = ['pipenv', 'install', '--deploy', '--system']
pipenv_command_dev = pipenv_command + ['--dev']


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    description = 'Post development installation with pipenv'
    user_options = []

    def run(self):
        subprocess.check_call(pipenv_command_dev)
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    description = 'Post production installation with pipenv'
    user_options = []

    def run(self):
        subprocess.check_call(pipenv_command)
        install.run(self)


class UploadCommand(upload):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        print('\033[1m{0}\033[0m'.format(s))

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(f'{base_dir}/dist')
        except FileNotFoundError:
            pass

        self.status('Building Source distribution...')
        subprocess.check_call([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])
        self.status('Uploading the package to PyPI via Twine...')
        subprocess.check_call(['twine', 'upload', 'dist/*'])
        self.status('Pushing git tags...')
        subprocess.check_call(['git', 'tag', f'v{version}'])
        subprocess.check_call(['git', 'push', '--tags'])


setup(
    name='jet-apispec',
    version=version,
    description='Jetfactory OpenAPI specification generator',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Robert Wikman',
    author_email='rbw@vault13.org',
    url='https://github.com/rbw/jet-apispec',
    packages=find_packages(exclude=['tests', 'tests.*']),
    entry_points={
        'console_scripts': [
        ]
    },
    package_data={
        '': ['LICENSE'],
    },
    python_requires='>=3.6',
    setup_requires=['pipenv'],
    include_package_data=True,
    license='BSD-2',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    cmdclass={
        'upload': UploadCommand,
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
