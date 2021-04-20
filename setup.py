from setuptools import setup, setuptools

setup(
    author='Justin Berthelot Sam Dominguez Daniel Munger Christopher Rice',
    author_email='pythoncov3rt@gmail.com',
    description='Covert Channel Management, Integration, and Implementation',
    entry_points={
        'console_scripts': ['cov3rt=cov3rt.command_line:runApplication']
    },
    install_requires=['scapy>=2.4.3', 
        'npyscreen>=4.10.0',
        'windows-curses>=2.2.0; platform_system == "Windows"'
    ],
    project_urls={
        'Documentation': 'https://github.com/jbert1/Cov3rt/blob/main/cov3rt-documentation.md',
        'Source Code': 'https://github.com/jbert1/Cov3rt/',
    },
    license='GPLv2',
    name='cov3rt',
    packages=setuptools.find_packages(),
    url='https://github.com/jbert1/Cov3rt/',
    version='1.0.1',
    zip_safe=False,
    long_description = """The cov3rt framework provides penetration testers and developers with a wide range of tools to manage, integrate, and deploy covert channel implementations.

Documentation is online at https://github.com/jbert1/Cov3rt/blob/main/cov3rt-documentation.md
"""
)
