---
title: "Working with the shared file system"
teaching: 15
exercises: 5
questions:
- "How do I store a file on node so that another node can see it?"
- "How do I store a file on node so that another node cannot see it?"
- "Do I really need scp for all of the above?"
objectives:
- "Submit a job that fills a file with arbitrary but known data and store it in the shared file system."
- "Submit a job that fills a file with arbitrary but known data and store it in the local file system of the execution host."
- "Raise the attention that a common file system also makes big problems common to all users very quickly."
key points:
- "A shared file system is one of the key components of modern HPC clusters."
- "`scp` and friends are rarely needed on a HPC cluster."
- "A shared file system is a resource for all users, so use it wisely to not affect others."
---

After all these first attempts to make use of the cluster, Lola wonders about something. If she submit's a job, how would she be able to store data and access it from her laptop?

Lola comes up with a small example job, that collects information on the node that the jobs is run on and submit's it.

~~~
{% include /snippets/02/submit_node_info.{{ site.workshop_scheduler }} %}
~~~
{: .bash }

When the job is done, she scans the current directory from where she submitted the job. But the file that she expects does not appear. Lola goes back to the script she wrote. There is one line that looks suspicious.

~~~
FILENAME=/tmp/`hostname`_info.log
~~~
{: .bash }

She checks the contents of `/tmp`. Nothing as well. That means that whereever Lola's script runs, the output is stored under `/tmp/` but not on the node where she submitted her job from. The problem is that this directory is local to the node where the script is run. There is no automated synchronisation, so the file will never appear on the machine where Lola is currently working.

> ## tmp
> This is the canonical Linux temporary directory where anyone (i.e. the operating system as well as any user or user application) is allowed to create, write, read and delete files and directories. The directory is typically cleared of any content when the node is rebooted.
{: .callout }

Lola asks her colleague how to proceed. He mentions that `{{ site.workshop_shared_fast_filesystem }}` is a directory that is a shared file system. In other words any directory under `{{ site.workshop_shared_fast_filesystem }}` is updated in real-time across the entire cluster. As the name suggests, this file system appears to be a very fast one. Her colleague notes it's a parallel file system.

> ## parallel file system
>
> Parallel file systems such as, [lustre](http://lustre.org/), [GPFS](https://www.ibm.com/support/knowledgecenter/en/SSFKCN/gpfs_welcome.html), [BeeGeeFS](http://www.beegfs.com/content/) etc, are the limbs of a multi-purpose HPC cluster. These file systems consist of a software layer that needs to be installed on all nodes of a cluster and dedicated hardware external to the compute nodes. The mere goal of these systems is to provide high bandwidth for writing and reading in parallel, i.e. from multiple nodes at the same time, of large volumes of data. If it wouldn't be for them, simulations and data analysis jobs would have nowhere to put their results or read their inputs from.

Lola doesn't bother with the technical details for a moment. She simply wants to get the job done. So she changes the offending line to:

~~~
FILENAME={{ site.workshop_shared_fast_filesystem }}/lola/`hostname`_info.log
~~~
{: .bash }

and submits the job. And voila, the file appears in `{{ site.workshop_shared_fast_filesystem }}/lola/` with the expected input: 

~~~
n01
             total       used       free     shared    buffers     cached
Mem:           125         87         38          0          0         67
-/+ buffers/cache:         19        106
Swap:            1          0          1
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 45
model name      : Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz
stepping        : 7
cpu MHz         : 2500.122
cache size      : 15360 KB
physical id     : 0
siblings        : 6
core id         : 0
cpu cores       : 6
apicid          : 0
initial apicid  : 0
fpu             : yes
fpu_exception   : yes
cpuid level     : 13
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx sm
x est tm2 ssse3 cx16 xtpr pdcm dca sse4_1 sse4_2 x2apic popcnt aes xsave avx lahf_lm ida arat epb xsaveopt pln pts dts tpr_shadow vnmi flexpriority ept vpid
bogomips        : 5000.24
clflush size    : 64
cache_alignment : 64
address sizes   : 46 bits physical, 48 bits virtual
# ...
~~~
{: .output }

Lola is happy. Before leaving, her colleague briefs her, that she should be cautious with this file system. Even though it appears so powerful, misusing it will effects on all other users as it is a **shared** file system.
