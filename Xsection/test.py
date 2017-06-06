#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 15:52:18 2017

@author: keith
"""
import numpy as np
A = np.loadtxt("Am_241_fission.txt",delimiter = ",",skiprows=1)
B = np.loadtxt("Am_241_capture.txt",delimiter = ",",skiprows=1)
print(A[0])
A = np.array_split(A,2)