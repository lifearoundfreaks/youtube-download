from operator import attrgetter

import exceptions
import const
from utils import is_int

WRONG_INPUT_EXCEPTION = exceptions.InputValidationException(
    f'Wrong input.\n\n{const.BOT_INPUT_TIP}'
)


def check_offset_validity(offset):

    if offset > const.MAX_VIDEO_SECONDS:
        raise exceptions.InputValidationException(
            f"Videos only up to {const.MAX_VIDEO_SECONDS} seconds are allowed."
        )
    elif offset <= 0:
        raise exceptions.InputValidationException(
            "Starting time cannot be larger or equal to ending time."
        )


class VideoTimecode:

    def __init__(self, code="0", **kwargs):

        split_input = self._split_func(code)

        process_function = {
            1: self._process_single,
            2: self._process_double,
            3: self._process_triple,
        }.get(len(split_input))

        if process_function is None:

            raise WRONG_INPUT_EXCEPTION

        hours, minutes, seconds = process_function(*split_input)

        hours += kwargs.get('hours', 0)
        minutes += kwargs.get('minutes', 0)
        seconds += kwargs.get('seconds', 0)

        self.hours = hours + minutes // 60 + seconds // 3600
        self.minutes = (minutes + seconds // 60) % 60
        self.seconds = seconds % 60

        if 'start' in kwargs:

            check_offset_validity(self - kwargs['start'])

    @property
    def timestamp(self):

        return f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}'

    def _split_func(self, string):

        return string.split(":")

    def _convert_time(self, string, maximum=60):

        try:

            value = int(string)
            if value > maximum or value < 0:
                raise ValueError
            return value

        except ValueError:

            raise WRONG_INPUT_EXCEPTION

    def _process_single(self, seconds):

        return 0, 0, self._convert_time(seconds)

    def _process_double(self, minutes, seconds):

        return 0, self._convert_time(minutes), self._convert_time(seconds)

    def _process_triple(self, hours, minutes, seconds):

        return (
            self._convert_time(hours, maximum=99),
            self._convert_time(minutes),
            self._convert_time(seconds),
        )

    def __sub__(self, other):

        seconds = self.hours * 3600 + self.minutes * 60 + self.seconds
        other_seconds = other.hours * 3600 + other.minutes * 60 + other.seconds
        return seconds - other_seconds


class Parser:

    TIME_OFFSET_TAG = 'time_offset'
    RESOLUTION_TAG = 'resolution'
    TIMESTAMP_TAG = 'timestamp'

    def __init__(self, input_string):

        split_input = self._split_func(input_string)

        process_function = {
            1: self._process_single,
            2: self._process_double,
            3: self._process_triple,
            4: self._process_quadruple,
        }.get(len(split_input))

        if process_function is None:

            raise WRONG_INPUT_EXCEPTION

        else:

            self.url, self.time_from, self.time_to, self.res = \
                process_function(*split_input)

    def all(self):

        return attrgetter('url', 'time_from', 'time_to', 'res')(self)

    def _get_default_start(self):

        return const.DEFAULT_TIME

    def _get_default_stop(self, start):

        return const.DEFAULT_TIME + const.MAX_VIDEO_SECONDS

    def _split_func(self, input_string):

        return input_string.split()

    def _resolve_ambiguous(self, ambiguous):

        if ambiguous[-1:] == 's' and is_int(ambiguous[:-1]):

            return self.TIME_OFFSET_TAG

        elif ambiguous[-1:] == 'p' and is_int(ambiguous[:-1]):

            return self.RESOLUTION_TAG

        else:

            return self.TIMESTAMP_TAG

    def _convert_time_offset(self, offset):

        result = int(offset[:-1])
        check_offset_validity(result)
        return result

    def _process_single(self, url):

        return (
            url,
            VideoTimecode(seconds=const.DEFAULT_TIME).timestamp,
            VideoTimecode(
                seconds=const.DEFAULT_TIME + const.MAX_VIDEO_SECONDS
            ).timestamp,
            const.BEST_RESOLUTION_TAG,
        )

    def _process_double(self, url, ambiguous):

        ambiguous_tag = self._resolve_ambiguous(ambiguous)

        if ambiguous_tag == self.TIME_OFFSET_TAG:
            return (
                url,
                VideoTimecode(seconds=const.DEFAULT_TIME).timestamp,
                VideoTimecode(
                    seconds=const.DEFAULT_TIME
                    + self._convert_time_offset(ambiguous)
                ).timestamp,
                const.BEST_RESOLUTION_TAG,
            )

        elif ambiguous_tag == self.RESOLUTION_TAG:
            return (
                url,
                VideoTimecode(seconds=const.DEFAULT_TIME).timestamp,
                VideoTimecode(
                    seconds=const.DEFAULT_TIME + const.MAX_VIDEO_SECONDS
                ).timestamp,
                ambiguous,
            )

        elif ambiguous_tag == self.TIMESTAMP_TAG:
            return (
                url,
                VideoTimecode(ambiguous).timestamp,
                VideoTimecode(
                    ambiguous, seconds=const.MAX_VIDEO_SECONDS
                ).timestamp,
                const.BEST_RESOLUTION_TAG,
            )

        raise WRONG_INPUT_EXCEPTION

    def _process_triple(self, url, ambiguous_time, ambiguous):

        time_tag = self._resolve_ambiguous(ambiguous_time)
        ambiguous_tag = self._resolve_ambiguous(ambiguous)

        end_timecode = VideoTimecode(seconds=const.MAX_VIDEO_SECONDS)
        if time_tag == self.TIMESTAMP_TAG:
            start_timecode = VideoTimecode(ambiguous_time)
            end_timecode = VideoTimecode(
                start_timecode.timestamp, seconds=const.MAX_VIDEO_SECONDS)
        elif time_tag == self.TIME_OFFSET_TAG:
            if ambiguous_tag != self.RESOLUTION_TAG:
                raise WRONG_INPUT_EXCEPTION
            start_timecode = VideoTimecode(seconds=const.DEFAULT_TIME)
            end_timecode = VideoTimecode(
                seconds=const.DEFAULT_TIME +
                self._convert_time_offset(ambiguous_time)
            )
        else:
            raise WRONG_INPUT_EXCEPTION

        res = const.BEST_RESOLUTION_TAG
        if ambiguous_tag == self.TIMESTAMP_TAG:
            end_timecode = VideoTimecode(ambiguous, start=start_timecode)

        elif ambiguous_tag == self.TIME_OFFSET_TAG:
            end_timecode = VideoTimecode(
                start_timecode.timestamp,
                seconds=self._convert_time_offset(ambiguous)
            )
        else:
            res = ambiguous

        return (url, start_timecode.timestamp, end_timecode.timestamp, res)

    def _process_quadruple(self, url, time_from, ambiguous, resolution):

        ambiguous_tag = self._resolve_ambiguous(ambiguous)
        if ambiguous_tag not in (self.TIME_OFFSET_TAG, self.TIMESTAMP_TAG):
            raise WRONG_INPUT_EXCEPTION

        start_timecode = VideoTimecode(time_from)
        end_timestamp = VideoTimecode(
            time_from, seconds=self._convert_time_offset(ambiguous)
        ).timestamp if ambiguous_tag == self.TIME_OFFSET_TAG else \
            VideoTimecode(ambiguous, start=start_timecode)

        return (
            url,
            start_timecode.timestamp,
            end_timestamp,
            resolution,
        )
