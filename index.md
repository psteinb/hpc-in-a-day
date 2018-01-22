---
layout: lesson
root: .
---

"High-performance computing" supercomputers have been around for longer than some of their users today. The first supercomputer, the [Cray-1](https://en.wikipedia.org/wiki/Cray-1), was setup in 1976 and was put in operation at Los Alamos National Laboratory. In the course of history, the design of supercomputers underwent several revolutions. Today, most universities and an increasing part of the industry in several domains exploit the computational power of clusters of interconnected servers.

These High-performance Computing (HPC) clusters are used for large scale data processing and data analysis, fine grained parallel calculations and simulations of ever increasing fidelity. This course material is meant to introduce learners to the core principles behind the using a HPC cluster, how to connect to it, how to dispatch jobs and retrieve their results, and how to program applications that can harness the full power of this machinery. 

Please note that this lesson uses Python 3 without the intent of claiming python to be the universal language for HPC. Python is merely used as a vehicle to convey concepts that due to the intuitiveness of the language should be easy to transport to other languages and domains.

> ## Prerequisites
>
> If you have already written small programs with a language of your choice and know the difference between a “variable” and a “function” and obtain a minimal knowledge of using the UNIX command line (e.g. if you have completed [shell-novice](https://swcarpentry.github.io/shell-novice/), you are good to go.
>
> This lesson guides you through the basics of using a computer cluster (or batch farm or supercomputer). If you're already comfortable with using systems like LSF, Slurm or PBS/Pro and have already run applications on a super computer or even wrote parallel applications to run on a cluster, you probably won't learn much from this lesson. But you are welcome to help the others as a technical assistant or contribute to this [course material](https://psteinb.github.io/hpc-in-a-day).
{: .prereq}
