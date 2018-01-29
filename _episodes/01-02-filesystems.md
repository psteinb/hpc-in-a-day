---
title: "Navigating Files and Directories"
teaching: 20
exercises: 10
questions:
- "How can I see what files and directories I have?"
- "How can I move between folders?"
- "How can I specify the location of a file or directory?"
objectives:
- "Explain the similarities and differences between a file and a directory."
- "Translate an absolute path into a relative path and vice versa."
- "Construct absolute and relative paths that identify specific files and directories."
- "Explain the steps in the shell's read-run-print cycle."
- "Identify the actual command, flags, and file names in a command-line call."
- "Demonstrate the use of tab completion, and explain its advantages."
keypoints:
- "The filesystem is responsible for managing information on the disk."
- "Information is stored in files, which are stored in directories (folders)."
- "Directories can also store other directories, which forms a directory tree."
- "`cd path` changes the current working directory."
- "`ls path` prints a listing of a specific file or directory; `ls` on its own lists the current working directory."
- "`pwd` prints the user's current working directory."
- "`whoami` shows the user's current identity."
- "`/` on its own is the root directory of the whole filesystem."
- "A relative path specifies a location starting from the current location."
- "An absolute path specifies a location from the root of the filesystem."
- "Directory names in a path are separated with '/' on Unix, but '\\\\' on Windows."
- "'..' means 'the directory above the current one'; '.' on its own means 'the current directory'."
- "Most files' names are `something.extension`. The extension isn't required, and doesn't guarantee anything, but is normally used to indicate the type of data in the file."
- "Most commands take options (flags) which begin with a '-'."
---

Now that Lola has learned to move files and directories to and from the cluster,
she wants to know how to move from folder to folder and explore their contents.
She also wants to know how to organize the files and folders for her project
on the cluster.

The part of the operating system responsible for managing files and directories
is called the **filesystem**.
It organizes our data into files,
which hold information,
and directories (also called "folders"),
which hold files or other directories.

Several commands are frequently used to
create, inspect, copy, move, rename, and delete files and directories.
Lola has already seen one of these commands:

~~~
$ ls
~~~
{: .bash}

~~~
this_weeks_canteen_menus  todays_canteen_menu_downloaded.pdf  todays_canteen_menu.pdf
~~~
{: .output}

`ls` prints the names of the files and directories in
the "current" directory in alphabetical order,
arranged neatly into columns.
We can make its output more comprehensible by using the **flag**
`-F`, which tells `ls` to add a trailing
`/` to the names of directories:

~~~
$ ls -F
~~~
{: .bash}

~~~
this_weeks_canteen_menus/  todays_canteen_menu_downloaded.pdf  todays_canteen_menu.pdf
~~~
{: .output}

`ls` has lots of other options. To find out what they are, we can type:

~~~
$ ls --help
~~~
{: .bash}

~~~
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.

Mandatory arguments to long options are mandatory for short options too.
  -a, --all                  do not ignore entries starting with .
  -A, --almost-all           do not list implied . and ..
      --author               with -l, print the author of each file
  -b, --escape               print C-style escapes for nongraphic characters
      --block-size=SIZE      scale sizes by SIZE before printing them; e.g.,
                               '--block-size=M' prints sizes in units of
                               1,048,576 bytes; see SIZE format below
.
.
.
.
~~~
{: .output}

Many bash commands, and programs that people have written that can be
run from within bash, support a `--help` flag to display more
information on how to use the commands or programs.

For more information on how to use `ls` we can type `man ls`.
`man` is the Unix "manual" command:
it prints a description of a command and its options,
and (if you're lucky) provides a few examples of how to use it.

We said that `ls` prints the contents of
the "current" directory - or the directory we are currently "in".
Let's find out exactly what that directory by
running a command called `pwd`
(which stands for "print working directory").

~~~
$ pwd
~~~
{: .bash}

~~~
/home/lola
~~~
{: .output}

Here,
the computer's response is `/home/lola`,
which is Lola's **home directory**:

> ## username Variation
>
> In this lesson, we have used the username `lola` (associated
> with our hypothetical scientist Lola) in example input and output throughout.  
> However, when
> you type this lesson's commands on your computer,
> you should see and use something different,
> namely, the username associated with the user account on your computer.  This
> username will be the output from `whoami`.  In
> what follows, `lola` should always be replaced by that username.  
{: .callout}

> ## Home Directory Variation
>
> The home directory path will look different on different operating systems.
> On Linux it may look like `/home/lola`,
> and on Windows it will be similar to `C:\Documents and Settings\lola` or
> `C:\Users\lola`.  
> (Note that it may look slightly different for different versions of Windows.)
> In future examples, we've used Mac output as the default - Linux and Windows
> output may differ slightly, but should be generally similar.  
{: .callout}

To understand what a "home directory" is,
let's have a look at how the filesystem as a whole is organized.  For the
sake of example, we'll be
illustrating the filesystem on our scientist Lola's computer.  After this
illustration, you'll be learning commands to explore your own filesystem,
which will be constructed in a similar way, but not be exactly identical.  

On Lola's computer, the filesystem looks like this:

![The Filesystem]({{ page.root }}/fig/filesystem.svg)

At the top is the **root directory**
that holds everything else.
We refer to it using a slash character `/` on its own;
this is the leading slash in `/home/lola`.

Inside that directory are several other directories:
`usr` (stands for Unix System Resources, and contains important files and folders needed by the operating system)
`bin` (some built-in programs are stored here),
`data` (for miscellaneous data files),
`home` (where users' personal directories are located),
`tmp` (for temporary files that don't need to be stored long-term),
and so on.

We know that our current working directory
`/home/lola` is stored inside `/home`
because `/home` is the first part of its name.
Similarly,
we know that `/home` is stored inside the root directory `/`
because its name begins with `/`.



> ## Slashes
>
> Notice that there are two meanings for the `/` character.
> When it appears at the front of a file or directory name,
> it refers to the root directory. When it appears *inside* a name,
> it's just a separator.
{: .callout}

Underneath `/home`,
we find one directory for each user with an account on Lola's machine,
her colleagues the Mummy and Wolfman.  

![Home Directories]({{page.root}}/fig/home-directories.svg)

The Mummy's files are stored in `/home/imhotep`,
Wolfman's in `/home/larry`,
and Lola's in `/home/lola`.  Because Lola is the user in our
examples here, this is why we get `/home/lola` as our home directory.  
Typically, when you open a new command prompt you will be in
your home directory to start.  

We can also use `ls` to see the contents of a different directory
than the current directory.
Let's take a
look at our `this_weeks_canteen_menus` directory by running
`ls -F this_weeks_canteen_menus`,
i.e.,
the command `ls` with the **arguments**
`-F` and `this_weeks_canteen_menus`.
The second argument --- the one *without* a
leading dash --- tells `ls` that
we want a listing of something other than our
current working directory:

~~~
$ ls -F this_weeks_canteen_menus
~~~
{: .bash}

~~~
canteen_menu_day_1.pdf  canteen_menu_day_2.pdf  canteen_menu_day_3.pdf  canteen_menu_day_4.pdf  canteen_menu_day_5.pdf
~~~
{: .output}

Your output should be a list of all the
files and **sub-directories** inside `this_weeks_canteen_menus`.

As Lola continues to do stuff on the cluster,
she will create many files and directories,
and these directories will have sub-directories,
which in turn will have their own sub-directories, and so on.
Organizing things hierarchically in this way
will help Lola keep track of her work:
it's possible to put hundreds of files in her home directory,
just as it's possible for her to pile hundreds of
printed papers on her desk,
but it's a self-defeating strategy.

Now, we will learn how to move around the filesystem,
i.e., change our "working" directory from the home directory
(`/home/lola`) to something else.
The command to change locations is `cd` followed by a
directory name to change our working directory.
`cd` stands for "change directory",
which is a bit misleading:
the command doesn't change the directory,
it changes the shell's idea of what directory we are in.

Let's say we want to move to the `this_weeks_canteen_menus`
directory we saw above.  We can
use the following command to get there:

~~~
$ cd this_weeks_canteen_menus
~~~
{: .bash}

Let's look at the output of `pwd` now:

~~~
$ pwd
~~~
{: .bash}

~~~
/home/lola/this_weeks_canteen_menus
~~~
{: .output}

If we run `ls` without arguments now,
it lists the contents of `/home/lola/this_weeks_canteen_menus`,
because that's where we now are:

~~~
$ ls -F
~~~
{: .bash}

~~~
canteen_menu_day_1.pdf  canteen_menu_day_2.pdf  canteen_menu_day_3.pdf  canteen_menu_day_4.pdf  canteen_menu_day_5.pdf
~~~
{: .output}

We now know how to go "down" a directory tree.
how do we go up?  We might try the following:

~~~
cd lola
~~~
{: .bash}

~~~
-bash: cd: lola: No such file or directory
~~~
{: .error}

But we get an error! Why is this?

With our methods so far,
`cd` can only see sub-directories inside your current directory.  There are
different ways to see directories above your current location; we'll start
with the simplest.  

There is a shortcut in the shell to move up one directory level
that looks like this:

~~~
$ cd ..
~~~
{: .bash}

`..` is a special directory name meaning
"the directory containing this one",
or more succinctly,
the **parent** of the current directory.
Sure enough,
if we run `pwd` after running `cd ..`, we're back in `/home/lola/`.

~~~
$ pwd
~~~
{: .bash}

~~~
/home/lola/
~~~
{: .output}

These then, are the basic commands for navigating the filesystem on your computer:
`pwd`, `ls` and `cd`.  Let's explore some variations on those commands.  What happens
if you type `cd` on its own, without giving
a directory?

Let's explore one more big idea before moving on to
creating, deleting, moving and renaming files and folders.
Let's change working directory to the `this_weeks_canteen_menus`:

~~~
$ cd `this_weeks_canteen_menus`
~~~
{: .bash}

and let's consider the problem of going "up" the the home directory
again. Previously, we did this using `cd ..`. But there's
another way to do this:

~~~
$ cd /home/lola
~~~
{: .bash}

In the above command, we specify the **absolute path**
to the home directory, indicated by the leading slash.
The leading `/` tells the computer to
follow the path from the root of the filesystem.
To understand the idea of an absolute path better,
let's now try to change our working directory back
to the `this_weeks_canteen_menus` directory.
We know that we can do this with:

~~~
$ cd this_weeks_canteen_menus
~~~
{: .bash}

But another command that would work is:

~~~
$ cd /home/lola/this_weeks_canteen_menus
~~~
{: .bash}

In the above, we specify the absolute path
to the `this_weeks_canteen_menus` directory,
i.e., the path beginning from the root directory.
This is in contrast to the **relative path** we used
earlier, which is the path beginning from the working directory.

### Creating, Deleting, Copying and Moving Directories

Now that Lola knows how to navigate the filesystem
and about relative and absolute paths,
she is ready to learn how to create, delete, copy, move and rename
directories.

| Action                      | Command                     |
| ----------------------------|-----------------------------|
| Create a directory          | `mkdir <path-to-directory>` |
| Remove a directory          | `rm -r <path-to-directory>` |
| Copy a directory            | `cp -r <path-to-source> <path-to-destination>` |
| Delete a directory          | `rm -r <path-to-directory>` |
| Move a directory            | `mv <path-to-directory> <path-to-destination>` |

The paths above can be relative or absolute.

### Lola's Pipeline: Organizing Files

Knowing just this much about files and directories,
Lola is ready to organize data files that her predecessors left to her. 
First,
she creates a directory called `iot-estimate-of-pi`
(to remind herself where the data came from).
Inside that,
she creates a directory called `2017-03-15`,
which is the date she started processing the samples.
She used to use names like `conference-paper` and `revised-results`,
but she found them hard to understand after a couple of years.
(The final straw was when she found herself creating
a directory called `revised-revised-results-3`.)

> ## Sorting Output
>
> Lola names her directories "year-month-day",
> with leading zeroes for months and days,
> because the shell displays file and directory names in alphabetical order.
> If she used month names,
> December would come before July;
> if she didn't use leading zeroes,
> November ('11') would come before July ('7'). Similarly, putting the year first
> means that June 2016 will come before June 2017.
{: .callout}

Each of her estimation samples is labeled according to her predecessors convention
with a unique ten-character ID,
such as "ESTPI01729A".
This is what she found in the lab notebook given to her to record the program, version, machine, and other characteristics of the sample,
so she decides to use it as part of each data file's name.
Since the assay machine's output is plain text,
she will call her files `ESTPI01729A.txt`, `ESTPI01812A.txt`, and so on.
All 1520 files will go into the same directory.

Now in her current directory `data-shell`,
Lola can see what files she has using the command:

~~~
$ ls iot-estimate-of-pi/2017-03-15/
~~~
{: .bash}

This is a lot to type,
but she can let the shell do most of the work through what is called **tab completion**.
If she types:

~~~
$ ls iot-
~~~
{: .bash}

and then presses tab (the tab key on her keyboard),
the shell automatically completes the directory name for her:

~~~
$ ls iot-estimate-of-pi/
~~~
{: .bash}

If she presses tab again,
Bash will add `2017-03-15/` to the command,
since it's the only possible completion.
Pressing tab again does nothing,
since there are 19 possibilities;
pressing tab twice brings up a list of all the files,
and so on.
This is called **tab completion**,
and we will see it in many other tools as we go on.

At this point, Rob is called for an emergency into the machine room. He apologizes to Lola and suggests that she takes a look at the wiki the computer center has or browse the internet for helpful videos. Lola is left a bit startled as she knows that the group she works for just bought their own small cluster. So there is no documentation what so ever. Lola leaves a bit uncertain for her office.

> ## Absolute vs Relative Paths
>
> Starting from `/home/amanda/data/`,
> which of the following commands could Amanda use to navigate to her home directory,
> which is `/home/amanda`?
>
> 1. `cd .`
> 2. `cd /`
> 3. `cd /home/amanda`
> 4. `cd ../..`
> 5. `cd ~`
> 6. `cd home`
> 7. `cd ~/data/..`
> 8. `cd`
> 9. `cd ..`
>
> > ## Solution
> > 1. No: `.` stands for the current directory.
> > 2. No: `/` stands for the root directory.
> > 3. No: Amanda's home directory is `/home/amanda`.
> > 4. No: this goes up two levels, i.e. ends in `/home`.
> > 5. Yes: `~` stands for the user's home directory, in this case `/home/amanda`.
> > 6. No: this would navigate into a directory `home` in the current directory if it exists.
> > 7. Yes: unnecessarily complicated, but correct.
> > 8. Yes: shortcut to go back to the user's home directory.
> > 9. Yes: goes up one level.
> {: .solution}
{: .challenge}

> ## Relative Path Resolution
>
> Using the filesystem diagram below, if `pwd` displays `/home/thing`,
> what will `ls ../backup` display?
>
> 1.  `../backup: No such file or directory`
> 2.  `2012-12-01 2013-01-08 2013-01-27`
> 3.  `2012-12-01/ 2013-01-08/ 2013-01-27/`
> 4.  `original pnas_final pnas_sub`
>
> ![Filesystem for Challenge Questions]({{ page.root }}/fig/filesystem-challenge.svg)
>
> > ## Solution
> > 1. No: there *is* a directory `backup` in `/home`.
> > 2. No: this is the content of `Users/thing/backup`,
> >    but with `..` we asked for one level further up.
> > 3. No: see previous explanation.
> >    Also, we did not specify `-F` to display `/` at the end of the directory names.
> > 4. Yes: `../backup` refers to `/home/backup`.
> {: .solution}
{: .challenge}

> ## `ls` Reading Comprehension
>
> Assuming a directory structure as in the above Figure
> (Filesystem for Challenge Questions), if `pwd` displays `/home/backup`,
> and `-r` tells `ls` to display things in reverse order,
> what command will display:
>
> ~~~
> pnas_sub/ pnas_final/ original/
> ~~~
> {: .output}
>
> 1.  `ls pwd`
> 2.  `ls -r -F`
> 3.  `ls -r -F /home/backup`
> 4.  Either #2 or #3 above, but not #1.
>
> > ## Solution
> >  1. No: `pwd` is not the name of a directory.
> >  2. Yes: `ls` without directory argument lists files and directories
> >     in the current directory.
> >  3. Yes: uses the absolute path explicitly.
> >  4. Correct: see explanations above.
> {: .solution}
{: .challenge}

> ## Exploring More `ls` Arguments
>
> What does the command `ls` do when used with the `-l` and `-h` arguments?
>
> Some of its output is about properties that we do not cover in this lesson (such
> as file permissions and ownership), but the rest should be useful
> nevertheless.
>
> > ## Solution
> > The `-l` arguments makes `ls` use a **l**ong listing format, showing not only
> > the file/directory names but also additional information such as the file size
> > and the time of its last modification. The `-h` argument makes the file size
> > "**h**uman readable", i.e. display something like `5.3K` instead of `5369`.
> {: .solution}
{: .challenge}

> ## Listing Recursively and By Time
>
> The command `ls -R` lists the contents of directories recursively, i.e., lists
> their sub-directories, sub-sub-directories, and so on in alphabetical order
> at each level. The command `ls -t` lists things by time of last change, with
> most recently changed files or directories first.
> In what order does `ls -R -t` display things? Hint: `ls -l` uses a long listing
> format to view time stamps.
>
> > ## Solution
> > The directories are listed alphabetical at each level, the files/directories
> > in each directory are sorted by time of last change.
> {: .solution}
{: .challenge}
