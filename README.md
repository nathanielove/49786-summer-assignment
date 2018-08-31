# 49786 Summer Assignment

> **Author**: Nathaniel SUN
>
> **Date**: Aug 30 2018

## Problem Description

Given a total of N elements, find the largest coverage we can get after removing one segment.

Example: 

> **Input**: [[5,9], [1,4], [3,7]]
>
> **Output**: 7
>
> **Explanation**: By removing [3,7], the remaining segments covers a total length of 7

Input format: the first line contains the length of the array; all following lines are the start and end of segments.

The example above corresponds to:

```
3
5 9
1 4
3 7
```

## Quickstart

First, copy the input files into `files/input` folder.

Then, run the main script:

```bash
python main.py
```

## Project Structure

### Directory Tree

```
.
├── files
│   ├── input
│   │   ├── 1.in
│   │   └── 2.in
│   └── output
│       ├── 1.out
│       └── 2.out
├── main.py
└── solution
    ├── __init__.py
    ├── algorithm.py
    ├── files.py
    ├── models.py
    └── settings.py
```

### Descriptions

| Module | Description | 
| --- | --- | 
| `files/` | Contains the input/output files
| `main.py` | The main script that processes all files in `files/input` and write the outputs into separate files in the `files/output` directory 
| `solution/settings.py` | Contains constants related to filenames/paths
| `soluiton/models.py` | Contains the `Segment` model class
| `solution/files.py` | Contains the `FileEngine` class as an intermediate layer between the raw files and `Segment` objects
| `solution/algorithm.py` | Contains the core dynamic-programming algorithm and a brute-force verifier

## System Design Highlights

### The `Segment` Class

The `Segment` class represents a segment (as a line in the input file), with a `start` and an `end`.

This class is designed to be a hashable and immutable model class (although the immutability usually cannot be enforced in Python).

In addition to `hash` and `equals`, it provides several useful functions:

| Function | Description | 
| --- | --- | 
| `size()` | Returns the size of the segment
| `covers(other)` | Tells if the current segment covers another segment
| `overlaps(other)` | Tells if the current segment overlaps with another segment
| `intersection(other)` | Return the intersection segment of the current and another segment 

### The `FileEngine` Class

Each `FileEngine` object is in charge of a **pair** of input/output files. 

An instance can be created by `FileEngine(file_id)`, and it provides two functions:

| Function | Description | 
| --- | --- | 
| `read()` | Read the raw input file and return a list of `Segment` objects
| `write(int)` | Write an integer to the output file

## Algorithm

### Pre-processing

#### Sort

First, we sort the `Segment`s array according to their start time. This can be achieved in $O(n log(n))$ time.

#### Remove Sub-segments

Then, for each `Segment` object in the sorted array, we remove all following segments that it covers. This can be achieved in $O(n)$ time.

#### Find Redundancy

If there exists an `segments[i]` such that `segments[i-1]` overlaps with `segments[i+1]`, we call `segments[i]` "redundant", because the overall coverage will NOT be affected after it is removed. 

If a redundant segment is found, we simply calculate and return the coverage of the remaining segments.

### Properties of Segment Array

After pre-processing, we have a segment array with some special properties. 

Consider any three consecutive segments in the array, `segments[i-1]`, `segments[i]` and `segments[i+1]`, the following properties can be ensured:

| Property | Explanation | 
| --- | --- | 
| `segments[i-1].start <= segments[i].start <= segments[i+1].start` | Sorted
| `segments[i-1].end < segments[i].end < segments[i+1].end` | NO sub-segments
| `segments[i-1].end < segments[i+1].start` | NO redundancy (in other words, `segments[i-1]` and `segments[i+1]` are disjoint)


With such properties, the coverage of remaining segments after removing a `segments[i]` can be calculated by an addition of:

* Total coverage from `segments[0]` to `segments[i-1]`
* Total coverage from `segments[i+1]` to `segments[-1]`

### Two-pass DP

The core algorithm uses a two-pass dynamic programming technique, once forward and another backward. 

There are two arrays: `forward` and `backward`.

`forward[i]` stores the total coverage from `segments[0]` to `segments[i]`, and `backward[i]` stores the total coverage from `segments[i]` to `segments[-1]` (both ends included).

Hence, the first element in `forward` should be the `size()` of the first segment.

Then, from the second segment, for each `segments[i]`, we compute the combined total coverage up until that element, `forward[i]`, using three values we already have:

* `segments[i-1]`
* `segments[i]`
* `forward[i-1]`

If `segments[i-1]` and `segments[i]` does NOT overlap, the current total coverage `forward[i]` can be calculated by `forward[i-1] + segments[i].size()`.

Otherwise, we need to calculate the `intersection` by calling `segments[i].intersection(segments[i-1])`, and then `forward[i] = forward[i-1] + segments[i].size() + intersection.size()`

After we fill up the `forward` array, we do the same in the reverse order to generate the `backward` array. 

Once we have both the `forward` and `backward` arrays, finding the maximum coverage is super easy. For any element in between (not the first/last), the total coverage without it is simply `forward[i-1] + backward[i+1]`.

Finally, we compare all coverages above and `forward[-2]`, `backward[1]` to get the maximum. 
