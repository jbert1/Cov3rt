# Cov3rt
> Simplified covert channel creation, management, and deployment

## Authors

Justin Berthelot

Samuel Dominguez

Daniel Munger (Team Lead)

Christopher Rice

# Contents
* [Installation](#installation)
  * [Pip PyPI](#pip-pypi)
  * [Pip Local](#pip-local)
  * [Windows](#windows)
* [Cloaks](#cloak)
  * [What is a Cloak](#what-is-a-cloak)
  * [Cloak Classifications](#cloak-classifications)
  * [Create Your Own Cloak](#create-your-own-cloak)
* [Features](#features)
  * [Plug-and-Play Covert Channels](#plug-and-play-covert-channels)
  * [Application](#application)
  * [Module](#module)
* [Future](#future)
  * [Passive Channels](#passive-channels)
  * [Cloak Evaluation](#cloak-evaluation)

# Installation
## Pip PyPI
The easiest way to install the cov3rt framework is from the Python Package Index. We recommend installing with superuser privileges to properly send and receive packets with Scapy. 
```
$ pip install cov3rt
```

## Pip Local
You can choose to download the latest development version through our GitHub. First clone the cov3rt repository.
```
$ git clone https://github.com/jbert1/Cov3rt.git
```
Then navigate to the `setup.py` script and install via pip. We again recommend installing with superuser privileges to properly send and receive packets with Scapy.
```
$ cd Cov3rt
$ pip install .
```

## Windows
Windows requires Npcap (or WinPcap) to send and receive packets with Scapy. If you do not already have Npcap installed, you can find and download the latest version at https://nmap.org/npcap/#download.

# Cloaks
## What is a Cloak
Cloaks are programmatic network covert channel implementations developed for the cov3rt framework. 

## Cloak Classifications
We utilize Dr. Steffen Wendzel's "[Pattern-Based Survey and Categorization of Network Covert Channel Techniques](https://dl.acm.org/doi/10.1145/2684195)" to define our cloak classifications. We are currently utilizing the Feb-05-2021 version of his team's [pattern collection](https://ih-patterns.blogspot.com/p/test.html).

## Create Your Own Cloak
While we provide pre-defined cloaks within the framework, we encourage the community to develop and integrate their own cloaks into the framework. You can view our [documentation](https://pypi.org/project/cov3rt/) for more information on cloak development.

# Features
## Plug-and-Play Covert Channels
Each cloak is modularized in a such a way that they can be interchanged within each import or deployment. We believe swapping covert channel implementations should be easy for network administrators to stress test their network covert channel detection capabilities.

## Application
The cov3rt framework features a traditional CLI as well as a Terminal User Interface (TUI) built with npyscreen. The TUI provides a much more robust user experience, and the CLI allows teams to quickly and easily deploy one-liners in the field. 

## Module
The cov3rt framework can be imported into your own scripts for covert communication methods. We provide a proof-of-concept team communication interface within the Tools folder in our repo. Implementing covert channels into existing communication workflows is as simple as importing a cloak and communicating over the covert channel. 

# Future
## Passive Channels
We have yet to test any passive covert channels in the cov3rt framework. As a future goal, we would like to implement a method for users to add their own passive covert channels to our framework.

## Cloak Evaluation
Network covert channels have multiple metrics that help define their effectiveness in the field. We would like to provide a script that shows metrics to the user such as bandwidth, ease-of-detection, and communication speed.
