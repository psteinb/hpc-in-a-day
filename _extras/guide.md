---
layout: page
title: "Instructor Notes"
---

# Instructor's Briefung

This document tries to describe what preparations are required of instructors to make the workshop work as smooth as possible. In order to build the materials for the workshop at your site, consult the `_config.yaml` file before you generate the site with `make site`. It contains the 'environment variables' that are specific to your workshop, such as the name of the login node, the root folder of the shared file system etc.

## Chapter 1

### Section 1, Taking the space shuttle

At some point a folder named `this_weeks_canteen_menus` will be needed under `/tmp/this_weeks_canteen_menus` on the login node. Make sure before the lesson, that this folder is present. [/home/rob/this_weeks_canteen_menus](filesystem/home/rob/this_weeks_canteen_menus) of this material contains synthesized pdfs of a computerized canteen if you wish. You can use either these or prepare the menu of the canteen as single pdf files per day you'll go for the workshop into in this folder.

### Section 2, Navigating Files and Directories

Make sure that for this lesson, that the contents of [filesystem](../filesystem) folder are available somewhere for the learners to download and unpack.

## Chapter 2

None so far.

## Chapter 3

### Section 4, Searching for Pi

Use the file [generate_scrambled_data.py](./code/03_parallel_jobs/generate_scrambled_data.py) to produce 16 files that comply to the files used in this section, e.g. : 

```
pi_estimate_01.data  pi_estimate_04.data  pi_estimate_07.data  pi_estimate_10.data  pi_estimate_13.data  pi_estimate_16.data
pi_estimate_02.data  pi_estimate_05.data  pi_estimate_08.data  pi_estimate_11.data  pi_estimate_14.data
pi_estimate_03.data  pi_estimate_06.data  pi_estimate_09.data  pi_estimate_12.data  pi_estimate_15.data
```
{: .output}

This could be done like so:

~~~
$ for i in `seq -f "%02.0f" 1 16`;do python3 ./generate_scrambled_data.py pi_estimate_${i}.data;done
~~~
{: .output}

At best, create directories for the each learner so that they don't get into each other's way.

Note, that this lesson is currently quite fragile as the i/o caching can easily get into the way of the learners. 
