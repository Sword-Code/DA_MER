
import os

from sym_link_setup import Settings

def link(src, dst):
    if os.path.exists(dst):
        if os.path.islink(dst):
            os.remove(dst)
        else:
            raise Exception(f'Cannot overwrite a not-symlink file {dst} with a link to {src}')
    os.symlink(src, dst)

def links(settings):
    link(settings.eof_src, settings.eof_dst)
    for var in settings.DAvars:
        link(settings.IC_src.format(var), settings.IC_dst.format(var))

def main():
    settings=Settings()
    links(settings)
    
if __name__ == "__main__":
    main()
