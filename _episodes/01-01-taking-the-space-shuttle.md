---
title: "Taking the space shuttle"
teaching: 45
exercises: 5
questions:
- "What is a super computer?"
- "Where is a super computer?"
- "How do I connect to it?"
- "How do I transfer data to and from it?"
objectives:
- "Use ssh to open an interactive shell on a cluster."
- "Inspect a directory with ls."
- "Transfer a file to the cluster."
- "Transfer files/folders from the cluster to your local machine."
keypoints:
- "Super computers do not have screens."
- "Super computers are setup in remote places."
- "Super computers can be reached with ssh."
- "Files are transferred using scp/rsync."
- "There is a difference between cloud and HPC."
---

Through out this material, we will assist Lola Curious over her shoulder while she is starting to work at the Institute of Things as a side job to earn some extra money. 

On the first day, her supervisor greets her friendly and welcomes her to the job. He explains what her task is and suggests her that she will need to use the HPC cluster on the campus. Lola has so far used her Laptop at home for her studies, so the idea of using a super computer appears a bit intimidating to her. Her supervisor notices her anxiety and tells her that she will receive an introduction to the super computer after she has requested an account on the cluster. The word _super computer_ however doesn't bring Lola to ease.

Lola walks to the IT department and finishes the paper work to get an account. One of the admins, called Rob, promises to sit down with her in the morning to show her the way around the machine. And as Lola expected, they don't own a super computer. Rob explains that Lola will use a small to mid-range HPC cluster.

> ## A Super Computer ?
> Generally, a super computer refers to the worlds fastest machines available irrespective of their design but with the limitations that they need to be general purpose. Smaller computers of similar design than the above are commonly referred to as High performance computing (HPC) farms, batch farms, HPC clusters etc. A list of the fastest super computers is available on [top500.org](https://www.top500.org/lists/).
{: .callout}

First of all, Rob asks Lola to connect to the super computer. Rob mentions that in the past, compute clusters were named after planets or moons as they often presented distant somewhat mythological places. One of Rob's first instructors then often said, that they would use the Space Shuttle (or `ssh` briefly) to reach that planet or moon. So Rob asks Lola to open a terminal on her laptop and type in the following commands:

~~~ 
$ ssh lola@{{ site.workshop_login_host }}
~~~
{: .bash}

~~~ 
Last login: Tue Mar 14 14:13:14 2017 from lolas_laptop
-bash-4.1$ 
~~~
{: .output}

Rob explains to Lola that she is using the secure shell or `ssh`. This establishes a temporary encrypted connection between Lola's laptop and `{{ site.workshop_login_host }}`. The word before the `@` symbol, e.g. `lola` here, is the user account name that Lola has access permissions for on the cluster. 

> ## Where do I get this `ssh` from ?
> On Linux and/or macOS, the `ssh` command line utility is typically pre-installed. Just open a terminal and you are good to go. At the time of writing, the openssh support on microsoft is still pretty [recent](https://blogs.msdn.microsoft.com/powershell/2017/12/15/using-the-openssh-beta-in-windows-10-fall-creators-update-and-windows-server-1709/). Alternatives to this are [putty](http://www.putty.org), [bitvise SSH](https://www.bitvise.com/ssh-client-download) or [mRemoteNG](https://mremoteng.org/). Download it, install it and open the GUI. They typically ask for your user name and the destination address or IP. Once provided, you will be queried for your password just like in the example above.
{: .callout}


Rob tells her to use a UNIX command called `ls` (for list directory contents) to have a look around. 

~~~ 
$ ls
~~~
{: .bash}

~~~ 
~~~
{: .output}

To no surprise, there is nothing in there. Rob asks Lola to issue a command to see on what machine she currently is on.

~~~ 
$ hostname
~~~
{: .bash}

~~~ 
{{ site.workshop_login_host }}
~~~
{: .output}

Lola wonders a bit what this may be about, that you need a dedicated command to tell you where you are, but Rob explains to her that he has so many machines under his responsibility, that the output of `hostname` is often very valuable.

> ## Am I in the cloud now?
> Not really, sorry. At the time of writing, there are a couple of distinctive features that separate cloud computing from HPC.
> + *HPC*:
>   + machines are always available, i.e. the URL or address that you give to ssh to doesn't change over time typically and the servers of an HPC infrastructure are operating 24/7 behind this address
>   + machines typically run so called bare metal operating systems, i.e. when you ssh into an HPC cluster, the operating system that you will use is the same one the server was booted into
> - *cloud*:
>   - instances have to be requested (albeit this can be automated) e.g. on a web page. Then a user will be supplied a URL or address to point ssh to.
>   - cloud instances are run in so called virtual machines, i.e. an operating system inside an operating system, this is one of the reasons why the performance of cloud instances can be inferior to HPC clusters
{: .callout}

Rob explains to Lola that she has to work with this remote shell session in order to run programs on the HPC cluster. Launching programs that open a Graphical User Interface (GUI) is possible, but the interaction with the GUI will be slow as everything will have to get transferred through the WiFi network her laptop is currently logged into. Before Rob continues, he suggests to leave the cluster node again. For this, Lola can type in `logout` or `exit`.

~~~ 
$ logout
~~~
{: .bash}

He continues to explain, that typically people perform computationally heavy tasks on the cluster and prepare files that contain the results or a subset of data to create final results on the individuals laptop. So communication to and from the cluster is done mostly by transferring files. For example, Rob asks Lola to use a [file of her liking]({{page.root}}/filesystem/home/rob/this_weeks_canteen_menus/todays_canteen_menu.pdf) and transfer it over. For this, he advises her to use the secure copy command, `scp`. As before, this establishes a secure encrypted temporary connection between Lola's laptop and the cluster just for the sake of transferring the files. After the transfer has completed, scp will close the connection again.

~~~ 
$ scp todays_canteen_menu.pdf lola@{{ site.workshop_login_host }}:todays_canteen_menu.pdf
~~~
{: .bash}

~~~ 
todays_canteen_menu.pdf                                              100%   28KB  27.6KB/s   00:00
~~~
{: .output}

She can now `ssh` into the cluster again and check, if the file has arrived after she just uploaded it:

~~~ 
$ ssh lola@{{ site.workshop_login_host }}
Last login: Tue Mar 14 14:17:44 2017 from lolas_laptop
-bash-4.1$ ls
~~~
{: .bash}

~~~ 
todays_canteen_menu.pdf
~~~
{: .output}

Great. Now, let's try the other way around, i.e. downloading a file from the cluster to Lola's laptop. For this, Lola has to swap the two arguments of the `scp` command she just issued.

~~~ 
$ scp lola@{{ site.workshop_login_host }}:todays_canteen_menu.pdf todays_canteen_menu_downloaded.pdf
~~~
{: .bash}

Lola notices how the command line changed. First, she has to enter the source (`lola@{{ site.workshop_login_host }}`) then put a `:` and continue with the path of the file she wants to download. After that, separated by a space, the destination has to be provided, which in this case is a file `todays_canteen_menu_downloaded.pdf` in the current directory.

~~~
todays_canteen_menu.pdf                                                100%   28KB  27.6KB/s   00:00
~~~
{: .output}

Lola has a look in the current directory and indeed `todays_canteen_menu_downloaded.pdf`. She opens it with her pdf reader and can tell that it contains indeed the same content as the original one. Rob explains that if she would have used the same name as the destination, i.e. `todays_canteen_menu.pdf`, `scp` would have overwritten her local copy.

To finish, Rob tells Lola that she can also transfer entire directories. He prepared a temporary directory on the cluster for her under `/tmp/this_weeks_canteen_menus`. He asks Lola to obtain a copy of the entire directory onto her laptop.

~~~ 
$ scp -r lola@{{ site.workshop_login_host }}:/tmp/this_weeks_canteen_menus .
~~~
{: .bash}

~~~ 
canteen_menu_day_2.pdf                                                 100%   28KB  27.6KB/s   00:00    
canteen_menu_day_3.pdf                                                 100%   28KB  27.6KB/s   00:00    
canteen_menu_day_5.pdf                                                 100%   28KB  27.6KB/s   00:00    
canteen_menu_day_4.pdf                                                 100%   28KB  27.6KB/s   00:00    
canteen_menu_day_1.pdf                                                 100%   28KB  27.6KB/s   00:00
~~~
{: .output}

The trailing `.` is a short-hand to signify the current working directory that Lola calls `scp` from. When inspecting the current directory, Lola sees the transferred directory:

~~~ 
$ ls
~~~
{: .bash}

~~~
this_weeks_canteen_menus/  todays_canteen_menu_downloaded.pdf  todays_canteen_menu.pdf
~~~
{: .output}

A closer look into that directory using the relative path with respect to the current one:

~~~ 
$ ls this_weeks_canteen_menus/
~~~
{: .bash}

reveals the transferred files.

~~~ 
canteen_menu_day_1.pdf  canteen_menu_day_2.pdf  canteen_menu_day_3.pdf  canteen_menu_day_4.pdf  canteen_menu_day_5.pdf
~~~
{: .output}

Rob suggests to Lola to consult the man page of `scp` for further details by calling:

~~~ 
$ man scp
~~~
{: .bash}


> ## All mixed up
>
> Lola needs to obtain a file called `results.data` from a remote machine that is called `safe-store-1`. This machine is hidden behind the login node `{{ site.workshop_login_host }}`. However she mixed up the commands somehow that are needed to get the file onto her laptop. Help her and rearrange the following commands into the right order!
>
> ~~~~~
> $ ssh lola@`{{ site.workshop_login_host }}`
> $ logout
> $ scp lola@`{{ site.workshop_login_host }}`:results.data .
> $ scp lola@safe-store-1:results.data .
> ~~~~~
> > ## Solution
> > ~~~~~
> > $ ssh lola@`{{ site.workshop_login_host }}`
> > $ scp lola@safe-store-1:results.data .
> > $ logout
> > $ scp lola@`{{ site.workshop_login_host }}`:results.data .
> > ~~~~~
> {: .solution}
{: .challenge}


> ## Who is hanging around ?
>
> The `w` utility displays a list logged-in users and what they are currently doing. Use it to check:
>
> 1. that nobody but yourself is logged into your laptop/desktop
> 2. that a lot of people use the login node of your cluster `{{ site.workshop_login_host }}`
{: .challenge}

> ## Where did they go ?
>
> Rob has a zip file stored under `/tmp/passwords.zip` on the login node of the cluser `{{ site.workshop_login_host }}`. He wants to unzip it on his laptop under `/important/passwords`. How does he do that?
>
> 
> 1.   
> ~~~~~
> $ ssh rob@{{ site.workshop_login_host }}
> $ unzip /tmp/passwords.zip
> ~~~~~
> 
> 2.  
> ~~~~~
> $ scp {{ site.workshop_login_host }}@rob:/tmp/passwords.zip .
> $ unzip passwords.zip
> ~~~~~
> 
> 3.  
> ~~~~~
> $ cd /important/passwords
> $ scp rob@{{ site.workshop_login_host }}:passwords.zip .
> $ unzip passwords.zip
> ~~~~~
> 
> 4.  
> ~~~~~
> $ cd /important/passwords
> $ scp rob@{{ site.workshop_login_host }}:/tmp/passwords.zip .
> $ unzip passwords.zip
> ~~~~~
> 
> > ## Solution
> > 
> > 1. No: Rob only unpacks the zip file, but does not transfer the unpacked files onto his laptop
> > 2. No: Rob mixed up the syntax for scpc
> > 3. No: Rob did not specify the correct path of `/tmp/passwords.zip` on the login node of the cluser `{{ site.workshop_login_host }}`
> > 4. Yes: you may also use `unzip foo.zip -d /somewhere` if you want to omit the first command
> {: .solution}
{: .challenge}


