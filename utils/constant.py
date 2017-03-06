# -*- coding:utf-8 -*-
# ***********************************************************#
#     File: Data template
#   Author: Myron
# ***********************************************************#


class Constant(object):

    EMPTY_STRING = ''
    EMPTY_FLOAT = 0.0
    EMPTY_LIST = list()
    EMPTY_DICT = dict()

    def __setattr__(self, key, value):
        raise ValueError('Could not set value to a constant!')

CONSTANT = Constant()

if __name__ == '__main__':
    print CONSTANT.EMPTY_FLOAT
