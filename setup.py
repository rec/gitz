from gitz import config
import setuptools


if __name__ == '__main__':
    manfiles = ['man/man1/%s.1' % i for i in config.COMMANDS]
    setuptools.setup(
        name='gitz',
        version=config.VERSION,
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/gitz',
        description='🗜 gitz - tiny useful git commands, some dangerous 🗜',
        long_description=open(str('README.rst')).read(),
        long_description_content_type='text/x-rst',
        license='MIT',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
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
