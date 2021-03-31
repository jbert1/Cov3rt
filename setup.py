from setuptools import setup, setuptools

setup(
    author='Justin Berthelot Sam Dominguez Daniel Munger Christopher Rice',
    author_email='author@email.com',
    description='Testing Install of cov3rt',
    entry_points={
        'console_scripts': ['cov3rt=cov3rt.command_line:runApplication']
    },
    install_requires=['scapy>=2.4.3', 'npyscreen>=4.10.0'],
    license='MIT',
    name='cov3rt',
    packages=setuptools.find_packages(),
    url='https://github.com/jbert1/Cov3rt',
    version='0.0.6',
    zip_safe=False
)
