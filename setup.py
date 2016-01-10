from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='nsqueue',
    version='1.0.0',
    description='Simple distributed task queue using NSQ',
    url='https://github.com/ulule/nsqueue',
    author='Ulule',
    author_email='tech@ulule.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
