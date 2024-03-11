from setuptools import find_packages, setup

setup(
    name="CWorldUML",
    version="0.2",
    description="UML Editor",
    readme = "README.md",
    python_requires = ">= 3.8",
    license = "MIT", 
    author="Ganga Acharya, Marshall Feng, Peter Freedman, Adam Glick-Lynch, Tim Moser",
    author_email='grachary@millersville.edu, mdfeng@millersville.edu, pwfreedm@millersville.edu, ahglickl@millersville.edu, timbmoser@gmail.com',
    url="https://github.com/mucsci-students/2024sp-420-CWorld.git",
    packages=find_packages(where='src'),
    include_package_data=True,
    package_dir={'': 'src'},
    install_requires = [
        "pyqt6",
        "pytest",
    ]
)