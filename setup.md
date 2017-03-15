---
layout: page
title: Setup
permalink: /setup/
---

## Software requirements

Please bring your laptop to the course. Your laptop should have a program called `ssh` or any clients thereof installed and ready for use.

### Linux

Please make sure that ssh is in your PATH or to install ssh with your distribution's package manager (like xterm, terminal, konsole, etc. available as well).

### macOS / OSX

`ssh` is typically preinstalled, however be sure to have a terminal program (like e.g. [iTerm](https://www.iterm2.com/) available as well).

### Windows

It depends on your version of windows how and if you have to install a terminal and/or a ssh client. Typically, [putty](http://www.putty.org), [bitvise SSH](https://www.bitvise.com/ssh-client-download) or [mRemoteNG](https://mremoteng.org/) are a good choices.


## Logging in

In this lesson, we will be working on the command-line on a remote computer.
This means that the commands we enter into the command-line will be run
on a different computer than our laptop/workstation.

The first step will be to connect to this computer.
This is known as a remote login.

If you run Mac OS X or any other Unix-based operating system on your machine,
you can log in remotely by opening a terminal and using the `ssh` command:

~~~
$ ssh username@{{ site.workshop_login_host }}
~~~

Make sure to change `username` to the username you will have on the remote machine. Also, please change `{{ site.workshop_login_host }}` to what your instructors tells you.

