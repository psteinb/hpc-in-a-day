---
layout: page
title: Setup
permalink: /setup/
---

## Logging in

In this lesson, we will be working on the command-line on a remote computer.
This means that the commands we enter into the command-line will be run
on a different computer than our laptop/workstation.

The first step will be to connect to this computer.
This is known as a remote login.

If you run Mac OS X or any other Unix-based operating system on your machine,
you can log in remotely by opening a terminal and using the `ssh` command:

~~~
$ ssh username@login.hpc.euphoria.edu
~~~

Windows instructions???

## Downloading the data

We will need to download some code and data for this lesson.
This data is available online to download as a `.zip` file.
and the next few commands will download this file and "unzip" it.
One of the first things we will cover in the lesson is how to
look at the files and folders that we download.

~~~
$ cd
$ wget <path-to-data.zip>
$ unzip <data.zip>
~~~

