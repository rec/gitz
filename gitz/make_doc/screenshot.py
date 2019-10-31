from pathlib import Path


def screenshot(fp, command):
    screenshot = 'img/%s-screenshot.png' % command
    if Path(screenshot).exists():
        print(file=fp)
        print('.. image::', screenshot, file=fp)
