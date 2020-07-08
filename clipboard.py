import subprocess
import sys

LINUX_PLATFORM = 'linux'
OSX_PLATFORM = 'darwin'
WIN_PLATFORM = 'win32'


def stringify(text):
    return str(text).encode('utf-8')


def copy_osx_pbcopy(text):
    p = subprocess.Popen(['pbcopy', 'w'],
                         stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=text)


def copy2clip(txt):
    text = stringify(txt)
    if sys.platform.lower().startswith(OSX_PLATFORM):
        copy_osx_pbcopy(text)
    else:
        raise NotImplemented('Not implemented for your OS')


if __name__ == '__main__':
    copy2clip(' 11111 ')
