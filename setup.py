import os
import setuptools

NAME = "homeautomationconnector"

DEPENDENCIES_ARTIFACTORY = ["gpiozero", 
                            "RPi.GPIO", # gpiozero - Pin factory raspy 4
                            "lgpio",    # gpiozero - Pin factory raspy 5: neueste gpiozero-Version sucht zuerst nach lgpio, danach ... RPi.GPIO
                            "suntime", 
                            "numpy"]


DEPENDENCIES_GITHUB = {
    # "https://github.com/srw2ho/tcpconnector.git": "",
    "https://github.com/srw2ho/mqttconnector.git": "",
    "https://github.com/srw2ho/ppmpmessage.git": "",
    "https://github.com/srw2ho/tomlconfig.git": "",
    # "https://github.com/srw2ho/smdmeter2ppmpconnector.git": "",
}


def generate_pip_links_from_url(url, version):
    """Generate pip compatible links from Socialcoding clone URLs

    Arguments:
        url {str} -- Clone URL from Socialcoding
    """
    package = url.split("/")[-1].split(".")[0]
    url = url.replace("https://", f"{package} @ git+https://")
    if version:
        url = url + f"@{version}"

    return url


# create pip compatible links
DEPENDENCIES_GITHUB = [
    generate_pip_links_from_url(url, version)
    for url, version in DEPENDENCIES_GITHUB.items()
]
DEPENDENCIES = DEPENDENCIES_ARTIFACTORY + DEPENDENCIES_GITHUB

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name=NAME,
    # version_format='{tag}.dev{commitcount}+{gitsha}',
    setuptools_git_versioning={
        "enabled": True,
    },
    author="srw2ho",
    author_email="",
    description="",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    package_data={},
    install_requires=DEPENDENCIES,
    setup_requires=[
        "setuptools-git-versioning<2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License" "Operating System :: OS Independent",
    ],
)
