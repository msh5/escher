import os
import sys

from escher.__version__ import __version__

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_VENDOR = os.sep.join([PROJECT_ROOT, 'vendor'])
sys.path.insert(0, PROJECT_VENDOR)
