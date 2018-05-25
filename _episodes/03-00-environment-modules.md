---
title: "Changing the Environment"
teaching: 20
exercises: 10
questions:
- "How to extend the software installation of a HPC cluster?"
objectives:
- "Change the environment to allow custom software installations."
- "Understand that environment changes can be user driven."
- "Use the module system to use pre-installed software packages."
keypoints:
- "An HPC cluster is a shared resource. As such, users are not allowed to use package managers and install additional packages on all nodes."
- "Software can still be installed in user-owned file system locations."
- "The shell environment can be changed to allow a user to run custom software."
- "Changing the environment is so common, that automated systems like the environment modules are used to manage that."
---

When Lola sits down to tackle her next project, she wants to get a feeling on what tooling is available on the cluster. She is a passionate `python3` developer and hence wants to see what modules are already installed on the cluster. To her suprise, she discovers that it's not there:

~~~
$ python3
~~~
{: .bash}

~~~
bash: python3: command not found
~~~
{: .output}

Quite frustrated about this she spins up the package manager of her choice and punches in the commands to install `python3` from the linux distribution repositories. However this returns something along the lines of:

~~~
Error: This command has to be run under the root user.
~~~
{: .output}

She starts digging into the documentation. No mention of this short coming, that she is unable to install software that she needs. Hence, she grabs the phone to confer about this with the cluster support. Eventually, a cluster support staff drops by her office and explains the situation. 

> ## A shared resource of a hundreds
>
> TODO: Illustrate the tension of a homogenous installation, custom drivers to parallel file systems and more on a cluster and why users cannot install packages as they would on a workstation or laptop.
{: .callout }

The support staff, named Lena, demonstrates to Lola how she can deal with the situation. First off, she drops a [small application]({{ page.root }}/code/03_parallel_jobs/fdate) into Lola's home directory.

> ## A fancy date
>
> When downloading [small application]({{ page.root }}/code/03_parallel_jobs/fdate), the file needs to be made executable. To do this, issue the following command:
>
> ~~~~
> chmod u+x ./fdate
> ~~~~
> {: .bash}
> 
> This small executable does nothing more as to append/prepend dashes to the output of `date`.
{: .callout }

Lena demostrates that inside the folder where `fdate` was downloaded, it can be executed:

~~~
$ ./fdate
~~~
{: .bash}

~~~
-----------------------------
Fri May 25 17:14:28 CEST 2018
-----------------------------
~~~
{: .output}

However, when omitting the leading `./`, the command doesn't work anymore.

~~~
$ fdate
~~~
{: .bash}

~~~
bash: fdate: command not found...
~~~
{: .output}

Lena explains, that for regular compute jobs that read some data from disk, perform analysis or computation on them and store the results on disk, running applications by specifying the relative/absolute directory to an application works just fine.  
