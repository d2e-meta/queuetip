from collections import deque
from itertools import count


class RecorderError(Exception):
    pass


class Reading:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def __repr__(self):
        return f"Reading(id={self.id!r}, data={self.data!r})"


class Recorder:
    def __init__(self):
        self._tapes = {}
        self._analyzers = {}
        self._ids = count(1)

    def create_tape(self, tape):
        if tape in self._tapes:
            raise RecorderError(f"tape already exists: {tape}")
        self._tapes[tape] = set()

    def attach_analyzer(self, analyzer, tape):
        if tape not in self._tapes:
            raise RecorderError(f"no such tape: {tape}")
        if analyzer in self._analyzers:
            raise RecorderError(f"analyzer already exists: {analyzer}")
        self._tapes[tape].add(analyzer)
        self._analyzers[analyzer] = deque()

    def inscribe(self, tape, data):
        if tape not in self._tapes:
            raise RecorderError(f"no such tape: {tape}")
        reading_id = str(next(self._ids))
        for analyzer in self._tapes[tape]:
            self._analyzers[analyzer].append(Reading(reading_id, data))
        return reading_id

    def replay(self, analyzer, max_readings=1):
        if analyzer not in self._analyzers:
            raise RecorderError(f"no such analyzer: {analyzer}")
        playhead = self._analyzers[analyzer]
        readings = []
        while playhead and len(readings) < max_readings:
            readings.append(playhead.popleft())
        return readings
