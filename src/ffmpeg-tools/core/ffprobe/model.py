# -*- coding=utf-8 -*-
r"""

"""
import pydantic
import typing as t
from pydantic import types
from fractions import Fraction


__all__ = ['FFProbe']


Tags: t.TypeAlias = t.Mapping[str, str]


def parse_fraction(value: str) -> t.Optional[Fraction]:
    from fractions import Fraction
    if value == "0/0": return Fraction()
    return Fraction(value)


class FFProbe(pydantic.BaseModel):
    streams: t.List[t.Union['VideoStream', 'AudioStream', 'SubtitleStream', 'DataStream']]
    chapters: t.List['Chapter']
    format: 'Format'

    @property
    def video_streams(self) -> t.List['VideoStream']:
        return [stream for stream in self.streams if isinstance(stream, VideoStream)]

    @property
    def main_stream(self) -> 'VideoStream':
        try:
            return next(stream for stream in self.streams if isinstance(stream, VideoStream))
        except StopIteration:
            raise IndexError("main stream not found")

    @property
    def audio_streams(self) -> t.List['AudioStream']:
        return [stream for stream in self.streams if isinstance(stream, AudioStream)]

    @property
    def subtitle_streams(self) -> t.List['SubtitleStream']:
        return [stream for stream in self.streams if isinstance(stream, SubtitleStream)]


class VideoStream(pydantic.BaseModel, arbitrary_types_allowed=True):
    index: int
    codec_name: str
    codec_long_name: str
    profile: str = None
    codec_type: t.Literal['video']
    codec_tag_string: str
    codec_tag: str
    width: int
    height: int
    coded_width: int
    coded_height: int
    closed_captions: bool
    has_b_frames: bool
    sample_aspect_ratio: str = None
    display_aspect_ratio: str = None
    pix_fmt: str
    level: int
    color_range: str = None
    color_space: str = None
    color_transfer: str = None
    color_primaries: str = None
    chroma_location: str = None
    is_avc: bool = None
    nal_length_size: int = None
    field_order: str = None
    refs: int
    r_frame_rate: Fraction
    avg_frame_rate: Fraction
    time_base: Fraction
    start_pts: int
    start_time: float
    disposition: 'Disposition'
    tags: Tags = pydantic.Field(default_factory=dict)

    @pydantic.field_validator('r_frame_rate', 'avg_frame_rate', 'time_base', mode='before')
    def parse_fractions(cls, v: str) -> Fraction:
        return parse_fraction(v)


class AudioStream(pydantic.BaseModel, arbitrary_types_allowed=True):
    index: int
    codec_name: str
    codec_long_name: str
    codec_type: t.Literal['audio']
    codec_tag_string: str
    codec_tag: str
    sample_fmt: str
    sample_rate: int
    channels: int
    channel_layout: str
    bits_per_sample: int
    dmix_mode: int = None
    ltrt_cmixlev: float = None
    ltrt_surmixlev: float = None
    loro_cmixlev: float = None
    loro_surmixlev: float = None
    r_frame_rate: Fraction
    avg_frame_rate: Fraction
    time_base: Fraction
    start_pts: int
    start_time: float
    bit_rate: int
    disposition: 'Disposition'
    tags: Tags

    @pydantic.field_validator('r_frame_rate', 'avg_frame_rate', 'time_base', mode='before')
    def parse_fractions(cls, v: str) -> Fraction:
        return parse_fraction(v)


class SubtitleStream(pydantic.BaseModel, arbitrary_types_allowed=True):
    index: int
    codec_name: str
    codec_long_name: str
    codec_type: t.Literal['subtitle']
    codec_tag_string: str
    codec_tag: str
    width: int
    height: int
    r_frame_rate: Fraction
    avg_frame_rate: Fraction
    time_base: Fraction
    start_pts: int
    start_time: float
    duration_ts: int = None
    duration: float = None
    disposition: 'Disposition'
    tags: Tags

    @pydantic.field_validator('r_frame_rate', 'avg_frame_rate', 'time_base', mode='before')
    def parse_fractions(cls, v: str) -> Fraction:
        return parse_fraction(v)


class DataStream(pydantic.BaseModel):
    index: int
    codec_name: str
    codec_long_name: str
    codec_type: t.Literal['data']
    codec_tag_string: str
    codec_tag: str


class AttachmentStream(pydantic.BaseModel):
    index: int
    codec_name: str
    codec_long_name: str
    codec_type: t.Literal['attachment']
    codec_tag_string: str
    codec_tag: str


class Chapter(pydantic.BaseModel, arbitrary_types_allowed=True):
    id: int
    time_base: Fraction
    start: int
    start_time: float
    end: int
    end_time: float
    tags: Tags

    @pydantic.field_validator('time_base', mode='before')
    def parse_fractions(cls, v: str) -> Fraction: return parse_fraction(v)


class Format(pydantic.BaseModel):
    filename: types.FilePath
    nb_streams: int
    nb_programs: int
    format_name: str
    format_long_name: str
    start_time: float
    duration: float
    size: int
    bit_rate: int
    probe_score: int
    tags: Tags


class Disposition(pydantic.BaseModel):
    default: bool
    dub: bool
    original: bool
    comment: bool
    lyrics: bool
    karaoke: bool
    forced: bool
    hearing_impaired: bool
    visual_impaired: bool
    clean_effects: bool
    attached_pic: bool
    timed_thumbnails: bool
