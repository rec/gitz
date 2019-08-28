import os

VERSION = '0.9.5'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
COMMANDS = sorted(f for f in os.listdir(ROOT_DIR) if f.startswith('git-'))
README = os.path.join(ROOT_DIR, 'README.rst')

if __name__ == '__main__':
    import setuptools

    setuptools.setup(
        name='gitz',
        version=VERSION,
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/gitz',
        description='🗜 gitz - tiny useful git commands, some dangerous 🗜',
        long_description=open(README).read(),
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
        include_package_data=True,
        keywords=['git'],
        scripts=COMMANDS,
        packages=setuptools.find_packages(exclude=['test']),
    )
