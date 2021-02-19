from setuptools import setup, setuptools

setup(
    name='cov3rt',
    version='0.0.6',
    description='Testing Install of cov3rt',
    url='https://github.com/jbert1/Cov3rt',
    author='Justin Berthelot Sam Dominguez Daniel Munger Christopher Rice',
    author_email='author@email.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires = ['scapy>=2.4.3','npyscreen'],
    entry_points = {
        'console_scripts': ['cov3rt=cov3rt.command_line:runApplication']
    },
    zip_safe=False
)
