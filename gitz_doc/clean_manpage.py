BACKTICK = '`'
NORMAL, OPEN_TICK, IN_TICK, CLOSE_TICK = range(4)
START, END = r'\fB', r'\fP'


def clean_line(line):
    def parts():
        state = NORMAL
        for i in line.replace('-', r'\-'):
            if i != BACKTICK:
                yield i

                if state is OPEN_TICK:
                    state = IN_TICK
                elif state is CLOSE_TICK:
                    state = NORMAL

            elif state is NORMAL:
                yield START
                state = OPEN_TICK

            elif state is IN_TICK:
                yield END
                state = CLOSE_TICK

    return ''.join(parts())


def clean_section(section):
    return [clean_line(i) for i in section]


def clean_sections(sections):
    return {k: clean_section(section) for k, section in sections.items()}
