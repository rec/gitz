from gitz import config


def _version():
    with open('gitz/config.py') as fp:
        line = next(i for i in fp if i.startswith('__version__'))
        return line.strip().split()[-1].strip("'")


if __name__ == '__main__':
    import setuptools

    with open('README.rst', 'rb') as fp:
        desc = fp.read()
    desc = desc.decode('utf-8')  # For Python 3.6

    manfiles = ['man/man1/%s.1' % i for i in config.COMMANDS]
    setuptools.setup(
        name='gitz',
        version=_version(),
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/gitz',
        description='🗜 gitz - tiny useful git commands, some dangerous 🗜',
        long_description=desc,
        long_description_content_type='text/x-rst',
        license='MIT',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Topic :: Utilities',
        ],
        include_package_data=True,
        keywords=['git'],
        scripts=config.COMMANDS,
        packages=setuptools.find_packages(exclude=['test']),
        data_files=[['man/man1', manfiles]],
    )
