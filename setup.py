import os
import setuptools

VERSION = '0.9.1'

setuptools.setup(
    name='gitz',
    version=VERSION,
    author='Tom Ritchford',
    author_email='tom@swirly.com',
    url='https://github.com/rec/gitz',
    description='🗜 gitz - tiny useful git commands, some dangerous 🗜',
    long_description=open('README.rst').read(),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
    ],
    keywords=['git'],
    scripts=[f for f in os.listdir('.') if f.startswith('git-')],
    py_modules=['_gitz'],
)
