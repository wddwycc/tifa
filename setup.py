from setuptools import setup

setup(
    name='tifa',
    version='0.1.0',
    packages=['tifa'],
    install_requires=['click'],
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
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Code Generators',
    ],
)
