from typing import Iterator


def segments(s: str) -> Iterator[str]:
    stack = ''
    for i in s:
        if i not in '+-' and stack and stack[-1] not in '+-':
            yield stack
            stack = ''
        stack += i
    if stack:
        yield stack


def segment_to_commits(segment: str) -> str:
    "a+b-c+d"
    assert len(segment) % 2 == 1, segment
    segment += '-'
    name, sign = zip(*(segment[i : i + 2] for i in range(0, len(segment), 2)))
    return ''.join(name), sign.index('-')


def segments_to_commits(s):
    for seg in segments(s):
        yield segment_to_commits(seg)
