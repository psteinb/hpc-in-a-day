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

> ## Important Notice for all learners
>
> The following material is based on a given cluster configuration at the time of writing. The notion, that python version 3 or higher is not the default python installed on your system may change in the future or change based on which system you are working on. 
>
> However, the rationale and use of environment modules remains untouched from this alteration. If it's not python3 you rely on, it maybe a higher version of perl, java, gcc, llvm/clang, etc.
{: .callout }

When Lola sits down to tackle her next project, she wants to get a feeling on what tooling is available on the cluster. She is a passionate `python3` developer and hence wants to see what modules are already installed on the cluster. To her surprise, she discovers that it's not there:

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
> HPC clusters are big monetary and human resource investments. As such, no one except the administrators are allowed to install software in the operating system that is run on tens or hundreds of compute nodes inside the cluster.
{: .callout }

The support staff, named Lena, demonstrates to Lola how she can deal with the situation. First off, she drops a [zip file with a small application]({{ page.root }}/code/02_parallel_jobs/fdate.zip) into Lola's home directory which Lola unpacks by calling `unzip fdate.zip`. This produces a small application named `fdate` in the current directory.

Lena demonstrates that inside the folder where `fdate` was unzipped, it can be executed:

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

Lena explains: When running a command, specifying the application to run by specifying the relative/absolute path works just fine. If you want to run the application from anywhere in the file system without specifying the exact path, further actions are required. 

Lola explains, that she wants `fdate` to work from anywhere and asks Lena to proceed and show her how to do it. Lena says that the situation is quite similar to a library when you want to find a book. Imagine the time when J.J.K. Rowling's books were in high demand. And let's imagine you are a clerk in a library which has an infinite amount of Harry Potter replica's available. How would you tame the constant high rate of people coming in and asking for the location of 'Harry Potter 7'? The tedious way would be to tell every customer, that they need to go to the upper level of the library, search for the fantasy corner and tend to the upper shelf of the last cabinet. This would resemble specifying the exact path to an application every time. 

What is likely to happen in a good library: a sign will be put up which tells a customer where books of high demand are. In the best of all worlds, there will be a guiding system which leads people to the fantasy corner. The same is possible on the command-line by expanding the `PATH` environment variable. `PATH` contains a set of file system locations (separated by a colon `:`) where the operating system is able to check for applications to run in the terminal. To print it, do 

~~~
$ echo ${PATH}
~~~
{: .bash}

which may yield something along the lines of:

~~~
/usr/lib64/ccache:/usr/local/bin:/usr/bin:/bin:/home/lola/bin:/usr/local/sbin:/usr/sbin
~~~
{: .output}

Many systems define `PATH` to yield some folders by default. It depends on the system configuration what you will see when running `echo ${PATH}` as above. That is a also a good thing in case you make an error when altering `PATH`, you simply leave the shell session by issuing `exit` or similar and can start from scratch next time you spin up the shell.

To proceed and make `/home/lola/from_lena/fdate` available to `PATH`, Lena shows Lola what to type:

~~~
$ export PATH=${PATH}:/home/lola/from_lena/
~~~
{: .bash}

As you can see only directories (not paths to files) are added to `PATH` (similar to the example above where only signs to the fantasy corner and not to Harry Potter V are put up). 

> ## A less cautious version
> 
> It is also fine to **prepend** an extension to `PATH`. 
> 
> ~~~~~
> $ export PATH=/home/lola/from_lena/:${PATH}
> ~~~~~
> {: .bash}
> 
> This means though that you have trust, that `/home/lola/from_lena/` does not contain applications which would shadow applications which are already accessible through `PATH`.
>
{: .callout }

> ## Making it work
>
> Lola wants to experiment herself and puts an application by the name of `lc` in `/home/lola/apps`. Which of the following commands adds that folder to PATH?
> 
> 1. `export PATH=/home/lola/apps`
> 2. `set PATH=/lola/home/apps;${PATH}`
> 3. `PATH=/lola/home/apps;${PATH}`
> 4. `export PATH=/home/lola/apps:$PATH`
>
> > ## Solution
> > 1. `export PATH=/home/lola/apps`  (NO: has side effects, removes all existing folders from PATH)    
> > 2. `set PATH=/lola/home/apps;${PATH}` (NO: does nothing and yields wrong separator ;)
> > 3. `PATH=/lola/home/apps;${PATH}`     (NO: only changes the PATH variable for this invocation, not persistent)
> > 4. `export PATH=/home/lola/apps:$PATH` (YES!)
> {: .solution}
{: .challenge}

> ## In the Shadows
>
> Something is broken in Lola's terminal. When using `ls`, she keeps getting 
> 
> ~~~~~
> -----------------------------
> Fri May 25 21:14:28 CEST 2018
> -----------------------------
> ~~~~~
> {: .output}
> 
> After she did the following:
>
> ~~~~~
> $ unzip fdate.zip
> $ export PATH=${PWD}:${PATH}
> $ cp fdate ls
> $ cd /tmp
> $ ls
> ~~~~~
> {: .bash} 
> 
> > ## Solution
> > `fdate.zip` can be downloaded from [here]({{ page.root }}/code/02_parallel_jobs/fdate.zip). 
> > Lola adds the path where `fdate` resides to `PATH`. By accident, she then copies fdate to a file named `ls`. As she preprended `$PWD` to `PATH`, this version of `ls` has precedence over `/usr/bin/ls` (the actual list command).
> {: .solution}
{: .challenge}


Lena is now able to use `fdate` wherever she wants.

~~~
$ cd ~
$ fdate
$ cd /tmp
$ fdate
~~~
{: .bash}

~~~
-----------------------------
Fri May 25 17:24:08 CEST 2018
-----------------------------
-----------------------------
Fri May 25 17:24:18 CEST 2018
-----------------------------
~~~
{: .output}

As the above is a very common task on HPC clusters and servers, elaborate systems to manage changing the environment have been introduced. One such system is called `environment modules`. Lena explains that this system is currently used on `{{ site.workshop_login_host }}`. 

To have a look, what software is available through the `module` system, a user invokes:

~~~
$ module available
~~~
{: .bash}

~~~
--------------------------------- /opt/modulefiles/ ---------------------------------------
python/3.6.5                pandoc/1.13.2               python_memory_profiler/0.31
fftw/3.3.4                  line_profiler/trunk         maven/3.0.5                 
#...
~~~
{: .output}

The structure of each entry is usually the same `<software>/<version>`, where `software` can be anything from a simple application to a larger framework. To help typing, issuing `module av` is enough. To make an application available, the `load` or `add` verb can be used interchangeably. In a new terminal window do:

~~~
$ module load python/3.6.5
~~~
{: .bash}

~~~
python version 3.6.5 for x86_64 architecture loaded.
~~~
{: .output}

The exact content of the above differs from system to system and depends on how the `module` system was configured. After doing so, `PATH` was changed so that `fdate` is now available. You can check now, that python is available now:

~~~
$ python --version             
~~~
{: .bash}

~~~
Python 3.6.5
~~~
{: .output}


> ## On some systems ...
> 
> The module load command doesn't replace `python` but rather makes `python3` or similar available. To check, try:
>
> ~~~
> $ python --version             
> ~~~
> {: .bash}
> 
{: .callout }

The real hallmark of the module system comes with the facility to switch off applications again by invoking:

~~~
$ module unload python/3.6.5
~~~
{: .bash}

When one tries again now, the above mentioned effect is gone again:

~~~
$ python --version
~~~
{: .bash}

~~~
Python 2.7.15
~~~
{: .output}


> ## The others do it too
> 
> The idea of programmatically changing the environment of a running terminal is offered by many other software stacks. In the python eco system, `virtualenv` is a prime example. of such. From the [`virtualenv` docs](https://virtualenv.pypa.io/en/stable/userguide/#activate-script):
>
> ~~~~~
> $ source bin/activate
> ~~~~~
> { .bash }
> 
> "... This will change your $PATH so its first entry is the virtualenv’s bin/ directory. (You have to use source because it changes your shell environment in-place.)"
> 
> Another prominent example are anaconda environments:
>
> ~~~~~
> $ conda create -n our_workshop python=3.6 numpy mpi4py line_profiler
> $ source activate our_workshop
> ~~~~~
> { .bash }
>
> The last line above changes the environment of the current shell, so that `python=3.6 numpy mpi4py line_profiler` are available.
{: .callout }

