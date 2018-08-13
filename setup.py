import sys
from os import path

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
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


__version__ = '0.0.3'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)
test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)

setup(
    author='Mustafa Caylak',
    author_email='mustafa.caylak@web.de',
    url='https://github.com/luxmeter/markone',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    description='Local web app to render your markdown files.',
    include_package_data=True,
    install_requires=requirements,
    keywords='flask web-app markdown renderer html',
    long_description=long_description,
    long_description_content_type="text/markdown",
    name='markone',
    packages=find_packages(exclude=['docs', 'tests*']),
    package_data={
        "markone": [
            "static/*",
            "static/**/*",
            "templates/*",
            "templates/**/*",
            "*.yaml",
        ]},
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
    version=__version__,
    license='Apache License 2.0'
)
