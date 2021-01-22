import setuptools

with open("README.md", 'r', encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cov3rt-LANTurtles", # TEMPORARY
    version="0.0.1",
    author="LAN Turtles (Justin B, Daniel M, Sam D, Christopher R)", # TEMPORARY
    author_email="INSERT EMAIL HERE", # TEMPORARY
    description="A covert channel deployment framework for pentesting teams", # TEMPORARY
    long_description=long_description,
    long_description_content_type="text/markdown", 
    url="https://github.com/jbert1/Cov3rt", # NOT SURE IF WE WANT TO INCLUDE THIS
    packages=setuptools.find_packages(),
    classifiers=[ # NEED VERIFICATION ON THIS
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)