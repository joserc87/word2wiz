from setuptools import setup

setup(name='word2wiz',
      version='0.2',
      description='A tool to create wizard configurations from word documents',
      url='http://github.com/joserc87/word2wiz',
      author='Jose Ramon Cano',
      author_email='jose.cano@theconsultancyfirm.com',
      license='MIT',
      packages=['word2wiz'],
      scripts=['bin/word2wiz'],
      zip_safe=False)
