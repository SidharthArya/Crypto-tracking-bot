import readline
import os
import datetime
import pickle
import requests
import threading
import readline
import time
import re
import os
import subprocess
import sys
import argparse
import marketoptions
import IPython

ipython = threading.Thread(target=IPython.embed)
ipython.start()
os.system("stty sane")

market_options = marketoptions.market_options
def handle_keyboard_interrupt():
        crypto.save_variables()
        os.system('stty sane')


class Crypto:
    def __init__(self, var_file=None):
        pass


