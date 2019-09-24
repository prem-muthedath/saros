#!/usr/bin/python

from .saros import Saros

if __name__ == "__main__":
    saros=Saros()
    print("SAROS REPOSITORY STATE BEFORE: \n" + saros.to_str())
    saros.link_revs()
    print("SAROS REPOSITORY STATE AFTER: \n" + saros.to_str())

