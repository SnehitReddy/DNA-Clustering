cdef extern from "diff.h":
    int get_min(int a, int b)
    int get_distance(char *sequenceA, char *sequenceB)

def py_get_distance(sequenceA: bytes, sequenceB: bytes) -> int:
    get_distance(sequenceA, sequenceB)

def py_get_min(a: int, b: int) -> int:
    get_min(a, b)
