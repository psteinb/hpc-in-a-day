---
title: "Estimation of Pi for Pedestrians"
teaching: 40
exercises: 10
questions:
- "How do I find the portion of a code snippet that consumes the longest time?"
objectives:
- "Perform an estimation of pi using only one CPU core."
- "Measure the run time of the serial implementation for this estimate of pi."
- "Find the line of code in a python program that took the longest."
keypoints:
- "Each programming language typically provides tools called profilers with which you can analyse the runtime of your code."
- "The estimate of pi spends most of it's time while generating random numbers."
- "The estimation of pi with the Monte Carlo method is a compute bound problem because pseudo-random numbers are just algorithms."
---

Lola is told that her predecessors all worked on the same project. A high performance calculation that is able to produce a high precision estimate of Pi. Even though calculating Pi can be considered a solved problem, this piece of code is used at the institute to benchmark new hardware. So far, the institute has only acquired larger single machines for each lab to act as a computational workhorse per group. But currently, the need for distributed computations has risen and hence a distributed code is needed, that yields both simplicity, efficiency and scalability. Simple!

The algorithm that Lola aims for was pioneered by _Georges-Louis Leclerc de Buffon_ in _1733_. 

![Estimating Pi with Buffon's needle]({{ page.root }}/tikz/estimate_pi.svg)

Overlay a unit square over a quadrant of a circle. Throw `m` random number pairs and count how many of the pairs lie inside the circle (the number pairs inside the circle is denoted by `n`). `Pi` is then approximated by: 

~~~
     4*m
Pi = ---
      n
~~~

The implementation of this algorithm using `total_count` random number pairs in a nutshell is given in the program below:

~~~
import numpy

np.random.seed(2017)

def inside_circle(total_count):
    
    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    filtered = np.where(radii<=1.0)
    count = len(radii[filtered])
    
    return count 
    
def estimate_pi(total_count):

    count = inside_circle(total_count)
    return (4.0 * count / total_count) 

~~~
{: .python}

For generating pseudo-random numbers, we sample the uniform probability distribution in the default floating point interval from `0` to `1`. The `sqrt` step is not required directly, but Lola includes it here for clarity. `numpy.where` is used obtain the list of indices that correspond to radii which are equal or smaller than `1.0`. At last, this list of indices is used to filter-out the numbers in the `radii` array and obtain its length, which is the number Lola are after.

Lola finishes writing the pi estimation and comes up with a [small python script]({{ page.root }}/code/03_parallel_jobs/serial_numpi.py), that she can launch from the command line:

~~~
$ python3 ./serial_numpi.py 1000000000
~~~
{: .bash}

~~~
[serial version] required memory 11444.092 MB
[serial version] pi is 3.141557 from 1000000000 samples
~~~
{: .output}

She must admit that the application takes quite long to finish. Yet another reason to use a cluster or any other remote resource for these kind of applications that take quite a long time. But not everyone has a cluster at his or her disposal. So she decides to parallelize this algorithm first so that it can exploit the number cores that each machine on the cluster or even her laptop has to offer.

## Premature Optimisation is the root of all evil!

Before venturing out and trying to accelerate a program, it is utterly important to find the hot spots of it by means of measurements. For the sake of this tutorial, we use the [line_profiler](https://github.com/rkern/line_profiler) of python. Your language of choice most likely has similar utilities.

If need be, to install the profiler, please issue the following command:
~~~
$ pip3 install line_profiler
~~~
{: .bash }

When this is done and your command line offers the `kernprof-3` executable, you are ready to go on. 

> ## Profilers
>
> Each programming language typically offers some open-source and/or free tools on the web, with which you can profile your code. Here are some examples of tools. Note though, depending on the nature of the language of choice, the results can be hard or easy to interpret. In the following we will only list open and free tools:
>
> - python: [line_profiler](https://github.com/rkern/line_profiler), [prof](https://docs.python.org/3.6/library/profile.html)
> - java script: [firebug](https://github.com/firebug/firebug)
> - ruby: [ruby-prof](https://github.com/ruby-prof/ruby-prof)
> - C/C++: [xray](https://llvm.org/docs/XRay.html), [perf](https://perf.wiki.kernel.org/index.php/Main_Page), 
> - R: [profvis](https://github.com/rstudio/profvis)
{: .callout }

Next, you have to annotate your code in order to indicate to the profiler what you want to profile. For this, we add the `@profile` annotation to a function definition of our choice. If we don't do this, the profiler will do nothing. So let's refactor our code a little bit:

~~~
def main():

    parser = argparse.ArgumentParser(description='Estimate Pi using a Monte Carlo method.')
    parser.add_argument('n_samples', metavar='N', type=int, nargs=1,
                        default=10000,
                        help='number of times to draw a random number')

    args = parser.parse_args()

    n_samples = args.n_samples[0]
    my_pi = estimate_pi(n_samples)
    sizeof = np.dtype(np.float32).itemsize

    print("[serial version] required memory %.3f MB" % (n_samples*sizeof*3/(1024*1024)))
    print("[serial version] pi is %f from %i samples" % (my_pi,n_samples))

    sys.exit(0)


if __name__=='__main__':
    main()
~~~

With this trick, we can make sure that we profile the entire application. Note, that this is a necessity when using `line_profiler`. We can now carry on, and annotate the main function.

~~~
...
@profile
def main():
  ...
~~~

Let's save this to `serial_numpi_annotated.py`. After this is done, the profiler is run with a reduced input parameter that does take only about 2-3 seconds:

~~~
$ kernprof-3 -l ./serial_numpi_annotated.py 50000000
[serial version] required memory 572.205 MB
[serial version] pi is 3.141728 from 50000000 samples
Wrote profile results to serial_numpi_annotated.py.lprof
~~~
{: .bash }

You can see that the profiler just adds one line to the output, i.e. the last line. In order to view, the output we can use the `line_profile` module in python:

~~~
$ python3 -m line_profiler serial_numpi_profiled.py.lprof
Timer unit: 1e-06 s

Total time: 2.07893 s
File: ./serial_numpi_profiled.py
Function: main at line 24

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    24                                           @profile
    25                                           def main():
    26         1            2      2.0      0.0      n_samples = 10000
    27         1            1      1.0      0.0      if len(sys.argv) > 1:
    28         1            3      3.0      0.0          n_samples = int(sys.argv[1])
    29                                           
    30         1      2078840 2078840.0    100.0      my_pi = estimate_pi(n_samples)
    31         1           11     11.0      0.0      sizeof = np.dtype(np.float32).itemsize
    32                                           
    33         1           50     50.0      0.0      print("[serial version] required memory %.3f MB" % (n_samples*sizeof*3/(1024*1024)))
    34         1           23     23.0      0.0      print("[serial version] pi is %f from %i samples" % (my_pi,n_samples)
~~~

Aha, as expected the function that consumes 100% of the time is `estimate_pi`. So let's remove the annotation from `main` and move it to `estimate_pi`:

~~~
    return count

@profile
def estimate_pi(total_count):

    count = inside_circle(total_count)
    return (4.0 * count / total_count)

def main():
    n_samples = 10000
    if len(sys.argv) > 1:
~~~

And run the same cycle of record and report:

~~~
$ kernprof-3 -l ./serial_numpi_annotated.py 50000000
[serial version] required memory 572.205 MB
[serial version] pi is 3.141728 from 50000000 samples
Wrote profile results to serial_numpi_annotated.py.lprof
$ python3 -m line_profiler serial_numpi_profiled.py.lprof
Timer unit: 1e-06 s

Total time: 2.0736 s
File: ./serial_numpi_profiled.py
Function: estimate_pi at line 19

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    19                                           @profile
    20                                           def estimate_pi(total_count):
    21                                           
    22         1      2073595 2073595.0    100.0      count = inside_circle(total_count)
    23         1            5      5.0      0.0      return (4.0 * count / total_count)
~~~
{: .output }

Ok, one function to consume it all! So let's rinse and repeat again and annotate only `inside_circle`.

~~~
@profile
def inside_circle(total_count):

    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    filtered = np.where(radii<=1.0)
    count = len(radii[filtered])

    return count
~~~

And run the profiler again:

~~~
$ kernprof-3 -l ./serial_numpi_annotated.py 50000000
[serial version] required memory 572.205 MB
[serial version] pi is 3.141728 from 50000000 samples
Wrote profile results to serial_numpi_annotated.py.lprof
$ python3 -m line_profiler serial_numpi_profiled.py.lprof
Timer unit: 1e-06 s

Total time: 2.04205 s
File: ./serial_numpi_profiled.py
Function: inside_circle at line 7

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     7                                           @profile
     8                                           def inside_circle(total_count):
     9                                           
    10         1       749408 749408.0     36.7      x = np.float32(np.random.uniform(size=total_count))
    11         1       743129 743129.0     36.4      y = np.float32(np.random.uniform(size=total_count))
    12                                           
    13         1       261149 261149.0     12.8      radii = np.sqrt(x*x + y*y)
    14                                           
    15         1       195070 195070.0      9.6      filtered = np.where(radii<=1.0)
    16         1        93290  93290.0      4.6      count = len(radii[filtered])
    17                                           
    18         1            2      2.0      0.0      return count
~~~

So generating the random numbers appears to be the bottleneck as it accounts for 37+36=73% of the total runtime time. 
So this is a prime candidate for acceleration.

> ## Word count
>
> Download [this python script]({{ page.root }}/downloads/count_pylibs.py) to your current directory. Run it by executing:
> 
> ~~~~~
> $ python3 count_pylibs.py
> 4231827 characters and 418812 words found in standard python libs
> ~~~~~
> {: .bash}
> 
> Use the `line_profile` module to find the hot spot in this program! 
> > ## Solution
> > 
> > ~~~~~
> > Timer unit: 1e-06 s
> > 
> > Total time: 0.334168 s
> > File: ./count_pylibs_annotated.py
> > Function: main at line 38
> > 
> > Line #      Hits         Time  Per Hit   % Time  Line Contents
> > ==============================================================
> >     38                                           @profile
> >     39                                           def main():
> >     40                                           
> >     41         1        63994  63994.0     19.2      text = load_text()
> >     42         1            5      5.0      0.0      nchars = len(text)
> >     43         1       270108 270108.0     80.8      nwords = word_count(text)
> >     44         1           53     53.0      0.0      print("%i characters and %i words found in standard python lib" % (nchars, nwords))
> >     45                                           
> >     46         1            2      2.0      0.0      if len(text):
> >     47         1            6      6.0      0.0          sys.exit(0)
> >     48                                               else:
> >     49                                                   sys.exit(1)
> > ~~~~~
> > The `word_count` function takes the longest time. Inside it, `re.split` hogs runtime the most.
> {: .solution}
{: .challenge}

> ## Faster is always better, right? (Part 1)
>
> Download [this python script]({{ page.root }}/downloads/count_pylibs.py) to your current directory. Run it by executing:
> 
> ~~~~~
> $ python3 count_pylibs.py
> 4231827 characters and 418812 words found in standard python libs
> ~~~~~
> {: .bash}
> 
> Find the hotspot of the application.
> 
> > ## Solution
> > The function which is evaluated most often is `word_count` as it is run on every python lib which is found in the current standard library.
> {: .solution}
{: .challenge}


> ## Faster is always better, right? (Part 2)
>
> Download [this python script]({{ page.root }}/downloads/count_pylibs.py) to your current directory. Run it by executing:
> 
> ~~~~~
> $ python3 count_pylibs.py
> 4231827 characters and 418812 words found in standard python libs
> ~~~~~
> {: .bash}
> 
> 1. Start a Stopwatch
> 2. Find one alternative way to achieve what `count_pylibs.py` does.
> 3. Run the application and check if you sped up your code
> 4. Stop your Stopwatch
> 5. Compare the time your invested versus the speed-up you obtained.
> 6. Review the [literature](https://xkcd.com/1205/) about this cycle.
{: .challenge}
