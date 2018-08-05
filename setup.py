import sys

from os import path
from codecs import open

from pipenv.utils import convert_deps_to_pip
from pipenv.project import Project

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


__version__ = '0.0.1'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)
test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)

setup(
    author='Mustafa Caylak',
    author_email='caylak@adobe.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    description='# TODO write description',
    include_package_data=True,
    install_requires=requirements,
    keywords='',
    # long_description=long_description,
    name='markone',
    packages=find_packages(exclude=['docs', 'tests*']),
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
    version=__version__,
)
