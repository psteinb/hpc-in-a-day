---
title: "Searching for the answer to life, the universe and everything"
teaching: 40
exercises: 10
questions:
- "How do I analyse a lot of large files efficiently?"
objectives:
- "Perform a Map-Reduce style operation to extract information from large files and collect these into one final answer."
key points:
- "Searching through a large file is bound by the speed that I can read-in the file."
- "Having a set of files, the result of searching one file is indepent of searching its sibling."
- "HPC clusters have very powerful parallel file systems, that offer the best speed if data is accessed in parallel."
- "The operation of searching through a file can be mapped to individual nodes on the cluster. (map step)"
- "After the map step has been completed, all sub-results have to be reduced to one final result. (reduce step)"
---

Lola comes to work the next day and finds that someone has completely messed up her files. Her home directory on the server looks like a someone threw dices with the characters of here file names. By coincidence, she also detects that the log files of the last day have increased by some orders of magnitude in size. She opens one of her files and finds out that the results are still there.
