'''
Galaxyctl
'''

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
  name='galaxyctl',
  version='0.1.0a1',
  description='galaxy,onedata and luks volume management',
  long_description=readme(),
  url='https://github.com/mtangaro/galaxyctl',
  author='Marco Antonio Tangaro, Federico Zambelli',
  author_email='ma.tangaro@ibiom.cnr.it', 
  license='MIT',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',
  ],
  keywords='galaxy web server',
  scripts=['bin/galaxyctl'],
)
