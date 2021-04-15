import unittest
from input_parser import VideoTimecode, Parser
from exceptions import InputValidationException
import const


class TestVideoTimecode(unittest.TestCase):

    def test_input_validation_exceptions(self):

        exception_cases = [
            (['84:21'], {}),
            (['10:21.5'], {}),
            ([':23'], {}),
            (['00:120'], {}),
            (['123:15:21'], {}),
            (['00:aa:15'], {}),
            (['string'], {}),
            (['1:1:1:1'], {}),
            ([''], {}),
        ]

        for args, kwargs in exception_cases:
            self.assertRaises(
                InputValidationException,
                VideoTimecode,
                *args, **kwargs
            )

    def test_output_values(self):

        tc = VideoTimecode(seconds=120)
        self.assertEqual(tc.seconds, 0)
        self.assertEqual(tc.minutes, 2)
        self.assertEqual(tc.hours, 0)
        tc = VideoTimecode("15:2", seconds=60)
        self.assertEqual(tc.seconds, 2)
        self.assertEqual(tc.minutes, 16)
        tc = VideoTimecode("10:15:2", minutes=46, seconds=3661)
        self.assertEqual(tc.seconds, 3)
        self.assertEqual(tc.minutes, 2)
        self.assertEqual(tc.hours, 12)


class TestParser(unittest.TestCase):

    def test_input_validation_exceptions(self):

        exception_cases = [
            'video_url 720',
            'video_url 10/20',
            f'video_url 10:20 {const.MAX_VIDEO_SECONDS+1}s',
            'video_url 15:21 15:20',
            'video_url 15:21 16:22',
            'video_url -5s',
            'video_url 25s 25s',
            'video_url 25s 00:05',
        ]

        for input_string in exception_cases:
            self.assertRaises(InputValidationException, Parser, input_string)

    def test_output_values(self):

        expected_results = [
            ('video_url', (
                'video_url', '00:00:00', '00:01:00',
            )),
            ('video_url 20s', (
                'video_url', '00:00:00', '00:00:20',
            )),
            ('video_url 15 25', (
                'video_url', '00:00:15', '00:00:25',
            )),
            ('video_url 00:15 25s', (
                'video_url', '00:00:15', '00:00:40',
            )),
            ('video_url 25s', (
                'video_url', '00:00:00', '00:00:25'
            )),
            ('video_url 0:15', (
                'video_url', '00:00:15', '00:01:15',
            )),
            ('video_url 00:0:15', (
                'video_url', '00:00:15', '00:01:15',
            )),
            ('video_url 01:00:15 59s', (
                'video_url', '01:00:15', '01:01:14',
            )),
        ]

        for parser_input, expected_outputs in expected_results:

            results = Parser(parser_input).all()

            for expected, actual in zip(expected_outputs, results):
                self.assertEqual(expected, actual)
