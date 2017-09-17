import os
import sys
from shutil import rmtree

from setuptools import setup, Command

here = os.path.abspath(os.path.dirname(__file__))


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(
            sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name='tifa',
    version='0.2.8',
    packages=['tifa'],
    install_requires=[
        'click==6.7',
        'Jinja2==2.9.6',
        'PyYAML==3.12',
        'voluptuous==0.10.5',
    ],
    tests_require=['pytest==3.2.2'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'tifa = tifa.cli:main'
        ]
    },
    url='https://github.com/wddwycc/tifa',
    license='MIT',
    author='duan',
    author_email='wddwyss@gmail.com',
    description='a modern flask scaffolding',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Code Generators',
    ],
    # $ setup.py publish support.
    cmdclass={
        'publish': PublishCommand,
    },
)
