# coding=utf-8
__author__ = 'xuxin'
import os

def organized_by(path, isdir, base, base_isdir):
    """是否路径path等于或属于路径base
    """
    relpath = os.path.relpath(path, base)
    if base_isdir:
        return not relpath.startswith('../')
    else:
        return not isdir and relpath == '.'

if __name__ == "__main__":
    dir1 = '/usr/local/'
    dir2 = '/usr/local/test/'
    dir3 = '/test2/'
    print organized_by(dir1,True,dir2,True)

