---
title: "Taking the space shuttle"
teaching: 15
exercises: 0
questions:
- "What is a super computer?"
- "Where is a super computer?"
- "How do I connect to it?"
objectives:
- "Use ssh to open an interactive shell on a cluster."
- "Inspect a directory with ls."
- "Transfer a file to the cluster."
- "Transfer from the cluster."
key points:
- "Super computers do not have screens."
- "Super computers are setup in remote places."
- "Super computers can be reached with ssh."
- "Files are transferred using scp/rsync."
- "There is a difference between cloud and HPC."
---

Through out this material, we will assist Lola Curious over her shoulder while she is starting to work at the Institute of Things as a side job to earn some extra money. 

On the first day, her supervisor greets her friendly and welcomes her to the job. He explains what her task is and suggests her that she will need to use the HPC cluster on the campus. Lola has so far used her Laptop at home for her studies, so the idea of using a super computer appears a bit intimitating to her. Her supervisor notices her anxiety and tells her that she will receive an introduction to the super computer after she has requested an account on the cluster. The word _super computer_ however doesn't bring Lola to ease.

Lola walks to the IT department and finishes the paper work to get an account. One of the admins, called Rob, promises to sit down with her in the morning to show her the way around the machine. And as Lola expected, they don't own a super computer. Rob explains that Lola will use a small to mid-range HPC cluster.

> ## A Super Computer ?
> Generally, a super computer refers to the worlds fastest machines available irrespective of their design but with the limitations that they need to be general purpose. Smaller computers of similar design than the above are commonly referred to as High performance computing (HPC) farms, batch farms, HPC clusters etc. A list of the fastest super computers is available on [top500.org](https://www.top500.org/lists/).
{: .callout}

First of all, Rob asks Lola to connect to the super computer. For this, Lola has to open a terminal on her Laptop and type in the following commands:

~~~ bash
ssh lola@{{ site.workshop_login_host }}
~~~

~~~ output
Last login: Tue Mar 14 14:13:14 2017 from lolas_laptop
-bash-4.1$ 
~~~

