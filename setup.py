import os

VERSION = '0.9.3'
ROOT_DIR = os.path.dirname(__file__)
COMMANDS = sorted(f for f in os.listdir(ROOT_DIR) if f.startswith('git-'))


if __name__ == '__main__':
    import setuptools

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
        scripts=COMMANDS,
        py_modules=['gitz'],
    )
