import unittest

from recorder import Recorder, RecorderError


class RecorderTest(unittest.TestCase):
    def setUp(self):
        self.r = Recorder()

    def test_inscribe_with_no_analyzers_is_discarded(self):
        self.r.create_tape("engine")
        self.r.inscribe("engine", "rpm=4200")
        self.r.attach_analyzer("late", "engine")
        self.assertEqual(self.r.replay("late"), [])

    def test_inscribe_fans_out_to_all_analyzers(self):
        self.r.create_tape("engine")
        self.r.attach_analyzer("vibration", "engine")
        self.r.attach_analyzer("thermal", "engine")
        self.r.inscribe("engine", "rpm=4200")

        vibration = self.r.replay("vibration")
        thermal = self.r.replay("thermal")

        self.assertEqual([x.data for x in vibration], ["rpm=4200"])
        self.assertEqual([x.data for x in thermal], ["rpm=4200"])

    def test_replay_is_destructive(self):
        self.r.create_tape("engine")
        self.r.attach_analyzer("vibration", "engine")
        self.r.inscribe("engine", "rpm=4200")

        self.assertEqual(len(self.r.replay("vibration")), 1)
        self.assertEqual(self.r.replay("vibration"), [])

    def test_replay_returns_up_to_max_readings_in_order(self):
        self.r.create_tape("engine")
        self.r.attach_analyzer("vibration", "engine")
        self.r.inscribe("engine", "first")
        self.r.inscribe("engine", "second")

        readings = self.r.replay("vibration", max_readings=2)

        self.assertEqual([x.data for x in readings], ["first", "second"])

    def test_replay_respects_max_readings_limit(self):
        self.r.create_tape("engine")
        self.r.attach_analyzer("vibration", "engine")
        self.r.inscribe("engine", "first")
        self.r.inscribe("engine", "second")

        self.assertEqual(len(self.r.replay("vibration", max_readings=1)), 1)
        self.assertEqual(len(self.r.replay("vibration", max_readings=5)), 1)

    def test_inscribe_returns_unique_reading_ids(self):
        self.r.create_tape("engine")
        self.r.attach_analyzer("vibration", "engine")
        id1 = self.r.inscribe("engine", "first")
        id2 = self.r.inscribe("engine", "second")

        self.assertNotEqual(id1, id2)
        self.assertEqual([x.id for x in self.r.replay("vibration", max_readings=2)], [id1, id2])

    def test_create_duplicate_tape_raises(self):
        self.r.create_tape("engine")
        with self.assertRaises(RecorderError):
            self.r.create_tape("engine")

    def test_attach_analyzer_to_missing_tape_raises(self):
        with self.assertRaises(RecorderError):
            self.r.attach_analyzer("vibration", "ghost")

    def test_attach_duplicate_analyzer_raises(self):
        self.r.create_tape("engine")
        self.r.attach_analyzer("vibration", "engine")
        with self.assertRaises(RecorderError):
            self.r.attach_analyzer("vibration", "engine")

    def test_inscribe_to_missing_tape_raises(self):
        with self.assertRaises(RecorderError):
            self.r.inscribe("ghost", "data")

    def test_replay_from_missing_analyzer_raises(self):
        with self.assertRaises(RecorderError):
            self.r.replay("ghost")


if __name__ == "__main__":
    unittest.main()
