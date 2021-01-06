# Cov3rt
> Covert channel management, integration, and implementation

## Authors

Justin Berthelot

Samuel Dominguez

Daniel Munger

Christopher Rice

# Contents
* [Cloaks] (#cloak)
  * [What is a Cloak] (#what-is-a-cloak)
  * [Cloak Classifications] (#cloak-classifications)
  * [Create Your Own Cloak] (#create-your-own-cloak)
* [Features] (#features)
  * [Plug-and-Play Covert Channels] (#plug-and-play-covert-channels)
  * [Dynamic and Static Analysis] (#dynamic-and-static-analysis)
  * [Application] (#application)
  * [Module] (#module)
* [Future] (#future)
  * [Network Analyzer] (#network-analyzer)
  * [Interpreter] (#interpreter)


## Cloaks

### What is a Cloak

A cloak is a covert channel implementation for the cov3rt framework.

### Cloak Classifications

Cloaks are classified by Stefen Wendzel's "Pattern-Based Survey and Categorization of Network Covert Channel Techniques" (https://dl.acm.org/doi/10.1145/2684195).

### Create Your Own Cloak

You can create your own cloaks!

## Features

The cov3rt framework supplies penetration testers and developers with a wide range of tools.

### Plug-and-Play Covert Channels

Each cloak is modularized in a such a way that they can be interchanged within the cov3rt framework.

### Dynamic and Static Analysis

Cloaks can be unveiled in a live environment or through the analysis of a capture file.

### Application

The cov3rt framework's application is used to quickly send or receive messages with pre-selected cloaks. 

### Module

The cov3rt framework can be imported into your own scripts for covert communication methods.

## Future

Here are our stretch-goals to integrate within the cov3rt framework!

### Network Analyzer

The network analyzer will inspect the current network environment or capture file and determine the best Cloak for covert communication.

### Interpreter

The cov3rt framework will feature an on-the-go interpreter for immediate access with the framework in a Python interpreter
