from setuptools import setup

import sys
if str(sys.version_info) < "3.6":
    sys.exit('Sorry, Python < 3.6 is not supported')

setup(
    name='kaomoji-cli',
    version='0.1',
    py_modules=['cli', 'clipboard'],
    entry_points={
        'console_scripts': [
            'kaomoji=cli:main',
            'kaomoji-cli=cli:main',
        ],
    },
)
