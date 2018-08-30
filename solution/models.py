class Segment(object):
    start = None
    end = None

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return 'Segment(start={start},end={end})'.format(start=self.start, end=self.end)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))

    def _check_type(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError('Type not compatible: {other}'.format(other=other))

    def covers(self, other):
        self._check_type(other)
        return self.start <= other.start and self.end >= other.end

    @staticmethod
    def sort_by_start(segments):
        segments.sort(key=lambda x: x.start)

    @staticmethod
    def _sorted_pair_by_start(a, b):
        segments = [a, b]
        Segment.sort_by_start(segments)
        return segments

    def overlaps(self, other):
        self._check_type(other)
        first, second = Segment._sorted_pair_by_start(self, other)
        return second.start < first.end

    def intersection(self, other):
        self._check_type(other)

        if not self.overlaps(other):
            raise ValueError('Segments do not overlap.')

        first, second = Segment._sorted_pair_by_start(self, other)
        return Segment(second.start, first.end)
