from setuptools import setup

setup(
    name='weppy-serve',
    version='0.1',
    packages=['weppy_serve', 'weppy_serve.commands'],
    include_package_data=True,
    install_requires=[
        'click',
        'weppy',
    ],
    entry_points='''
        [console_scripts]
        wserve=weppy_serve.cli:cli
    ''',
)
