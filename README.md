# HPC-in-a-day [![DOI](https://zenodo.org/badge/83803821.svg)](https://zenodo.org/badge/latestdoi/83803821)

Novice introduction to high performance computing. This material was conceived as a sandbox project for [swcarpentry/hpc-novice](https://github.com/psteinb/hpc-in-a-day). Parts of it will be contributed to [swcarpentry/hpc-novice](https://github.com/psteinb/hpc-in-a-day) in due course.

## Material

The material can be viewed [here](https://psteinb.github.io/hpc-in-a-day)!

## Audience

The material as such targets future users of a HPC infrastructure of any discipline. The learners are expected to have an introductory level of programming skills and should know their way around the UNIX command line on a beginners level as well.

## Scheduler

hpc-in-a-day is scheduler agnostic. Currently, it supports LSF and SLURM. The job scheduler type can be set with the `workshop_scheduler` variable in [_config.yaml](https://github.com/psteinb/hpc-in-a-day/blob/711cf3f309a04d4a6e955e39c701444733194fed/_config.yml#L40).

# How to build

## Dependencies

The material is based on the [software carpentry lesson template](https://github.com/swcarpentry/styles). It hence depends on a fairly recent version of [jekyll](jekyllrb.org). Just give building it with `make site` in the root directory a try. If you find any problems, please open an issue.
