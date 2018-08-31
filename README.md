# 49786 Summer Assignment

| Title |  49786 Summer Assignment | 
| --- | --- | 
| **Author** | **Nathaniel SUN**
| **Date** | **Aug 30 2018**

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
| `overlaps(other)` | Tells if the current segment overlaps another segment
| `intersection(other)` | Return the intersection segment of the current and another segment 

### The `FileEngine` Class

Each `FileEngine` object is in charge of a single input file. 

An object can be created by a call to the constructor: `FileEngine(file_id)`, and it provides two functions:

| Function | Description | 
| --- | --- | 
| `read()` | Read the raw input file and return a list of `Segment` objects
| `write()` | Write an integer to the output file

## Algorithm

### Sorting

First, we sort the `Segment`s array according to their start time. This can be achieved in $O(n log(n))$ time.

### Remove Sub-segments

Then, for each `Segment` object in the sorted array, we remove all following segments that it covers. This can be achieved in $O(n)$ time.

### Two-pass DP

The core algorithms follows a two-pass dynamic programming approach, once forward and another backward.

First, we create an array called `forward`. The first element in this array should be the `size()` of the first segment.

Then, from the second segment, for each `segments[i]`, we compute the combined total coverage up until that element, `forward[i]`, using three values we already have:

* `segments[i-1]`
* `segments[i]`
* `forward[i-1]`

If `segments[i-1]` and `segment[i]` does NOT overlap, the current total coverage `forward[i]` can be calculated by `forward[i-1] + segments[i].size()`.

Otherwise, we need to calculate the `intersection` by calling `segment[i].intersection(segment[i-1])`, and then `forward[i] = forward[i-1] + segment[i].size() + intersection.size()`

After we fill up the `forward` array, we reverse the segments array and do the same, in order to generate the `backward` array. 

Once we have both the `forward` and `backward` arrays, finding the maximum coverage is super easy. For any element in between (not the first/last), the total coverage without it is simply `forward[i-1] + backward[i+1]`.

Finally, we compare all coverages above and `forward[-2]`, `backward[1]` to get the maximum. 
