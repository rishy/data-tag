#! /usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import local

def installDep():
    local('flask/bin/pip install -r requirements.txt')

def runapp():
    local('flask/bin/python run.py')

