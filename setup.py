from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

version = {}
with open("word2wiz/version.py") as fp:
    exec(fp.read(), version)

setup(
    name='word2wiz',

    version=version['__version__'],

    description='A tool to create wizard configurations from MS word documents',
    long_description=long_description,

    url='http://github.com/joserc87/word2wiz',

    author='Jose Ramon Cano',
    author_email='jose.cano@theconsultancyfirm.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='word2wiz document-wizard docwiz spell',

    packages=['word2wiz'],

    install_requires=['Flask', 'Jinja2', 'python-docx'],

    extras_require={
        'test': ['behave'],
    },

    package_data={
        'word2wiz': ['*.txt', 'spell/*.spl']
    },

    entry_points={
        'console_scripts': [
            'word2wiz=word2wiz:main',
        ],
    },
)
