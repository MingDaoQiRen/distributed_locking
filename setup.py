from setuptools import setup, find_packages


def read_requirements():
    req_path = "./requirements.txt"
    with open(req_path) as req_file:
        return list(map(lambda x: x.strip(), req_file.readlines()))


if __name__ == '__main__':
    pkgs = find_packages()
    pkg_dirs = {'distributed_locking'}
    pkgs = list(filter(lambda pkg: pkg.split('.')[0] in pkg_dirs, pkgs))

    setup(
        name="distributed_locking",
        version="0.1.0",
        description="This is a demo package which should not be installed",
        author="YaSong Li",
        author_email="940016596@qq.com",
        packages=pkgs,
        install_requires=read_requirements()
    )
