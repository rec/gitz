from gitz import config

if __name__ == '__main__':
    import setuptools

    setuptools.setup(
        name='gitz',
        version=config.VERSION,
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/gitz',
        description='🗜 gitz - tiny useful git commands, some dangerous 🗜',
        long_description=open(str(config.README)).read(),
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
        scripts=config.COMMANDS,
        packages=setuptools.find_packages(exclude=['test']),
    )
