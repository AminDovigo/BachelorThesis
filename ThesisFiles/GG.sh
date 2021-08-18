#!/bin/bash
export PATH="/home/dovigoamin/miniconda3/bin:${PATH}"
source activate ad_conda_pyomo

str='2000b0500l4000d5.txt'
#echo $str
python modelloaggconcrete.py $str
