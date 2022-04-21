# Python script to call before running mainPI.py
import subprocess
subprocess.call('python3 -m http.server --directory "/home/cmps-375/Desktop/"', shell=True)