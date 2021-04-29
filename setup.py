from setuptools import setup, setuptools
from os import path as os_path
from io import open as io_open

# Return our GitHub documentation
def return_description():
    # Get the path of our documentation
    fpath = os_path.join(os_path.dirname(__file__), "cov3rt-documentation.md")
    # Open and read the file contents
    f = io_open(fpath, encoding="utf-8")
    data = f.read()
    f.close()
    # Return the contents
    return data

setup(
    author='Justin Berthelot Sam Dominguez Daniel Munger Christopher Rice',
    author_email='pythoncov3rt@gmail.com',
    description='Covert Channel Management, Integration, and Implementation',
    entry_points={
        'console_scripts': ['cov3rt=cov3rt.command_line:runApplication']
    },
    python_requires='>=3.6.0',
    install_requires=['psutil>=5.6.0',
        'scapy>=2.4.0',
        'npyscreen>=4.9',
        'windows-curses>=1.0; platform_system == "Windows"'
    ],
    project_urls={
        'Documentation': 'https://github.com/jbert1/Cov3rt/blob/main/cov3rt-documentation.md',
        'Source Code': 'https://github.com/jbert1/Cov3rt/',
    },
    license='GPLv2',
    name='cov3rt',
    packages=setuptools.find_packages(),
    url='https://github.com/jbert1/Cov3rt/',
    version='1.0',
    zip_safe=False,
    long_description_content_type='text/markdown',
    long_description=return_description()
)
