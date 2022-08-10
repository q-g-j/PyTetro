# -*- coding: utf-8 -*-

import os
import sys


class Common:
    @staticmethod
    def get_script_path():
        if hasattr(sys, '_MEIPASS'):
            return getattr(sys, '_MEIPASS') + "/"
        else:
            return os.path.abspath(".") + "/"
