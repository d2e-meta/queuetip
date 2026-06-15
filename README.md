# BlackBox

A lightweight, in-memory **flight-data recorder**, written in Python.

Sensors *inscribe* readings onto named **tapes**. Independent offline **analyzers** *replay* each tape at their own pace — every analyzer keeps its own **playhead**, so a slow analyzer never holds up a fast one.

## Usage

```python
from recorder import Recorder

r = Recorder()

r.create_tape("engine")
r.attach_analyzer("vibration", "engine")
r.attach_analyzer("thermal", "engine")

r.inscribe("engine", "rpm=4200")

r.replay("vibration")   # -> [Reading(id='1', data='rpm=4200')]
r.replay("thermal")     # -> [Reading(id='1', data='rpm=4200')]   each analyzer sees the reading
r.replay("vibration")   # -> []   each analyzer advances its own playhead
```

## API

| Method | Behavior |
|--------|----------|
| `create_tape(tape)` | Register a new tape. Raises `RecorderError` if it already exists. |
| `attach_analyzer(analyzer, tape)` | Attach an analyzer to a tape. Raises `RecorderError` if the tape is missing or the analyzer already exists. |
| `inscribe(tape, data)` | Record a reading onto the tape for every attached analyzer; returns the reading id. Raises `RecorderError` if the tape is missing. |
| `replay(analyzer, max_readings=1)` | Advance the analyzer's playhead, returning up to `max_readings` readings (`[]` if none). Raises `RecorderError` if the analyzer is missing. |

## Current scope

This is the in-memory core. A tape retains a reading only for the analyzers attached at the moment it is inscribed, and replaying advances that analyzer's playhead past the reading.

## Roadmap

1. **Now** — in-memory recorder (this version)
2. **Durable tapes** — append readings to on-disk tapes using length-prefixed records, so they survive a restart
3. **Persistent playheads** — each analyzer's position is saved to disk and resumes after a power loss
4. **Crash recovery** — a torn tail (a reading half-written when power dropped) is detected and discarded on restart, while every fully-written reading before it stays readable
5. Later — per-reading checksums / tamper-evident chaining, retention policies

## Running the tests

```bash
python3 -m unittest test_recorder -v
```

## License

[MIT](LICENSE).
