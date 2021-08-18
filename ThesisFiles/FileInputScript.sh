#!/bin/bash

export PATH="/home/dovigoamin/miniconda3/bin:${PATH}"
source activate ad_conda_pyomo

#books=(2000)
books=(20 40 100 200 500 1000 2000 5000 9999) #numero di libri posssibili
#n=(4 5)
n=(1 2 3 4 5) #numero istanze identiche con set diversi

onez="0"
twoz="00"
threez="000"
b="b"
l="l"
d="d"
for i in "${n[@]}" ; do
	for j in "${books[@]}" ; do
		libs=($((j/10)) $((j/4)))
		for w in "${libs[@]}" ; do 
			str=""
			if [[ $j -lt 100 ]] ; then
				str+="$twoz$j$b"
			elif [[ $j -lt 1000 ]] ; then
				str+="$onez$j$b"
			else
				str+="$j$b"
			fi
			if [[ $w -lt 10 ]] ; then
				str+="$threez$w$l"	
			elif [[ $w -lt 100 ]] ; then
				str+="$twoz$w$l"
			elif [[ $w -lt 1000 ]] ; then
				str+="$onez$w$l"
			else
				str+="$w$l"
			fi
			count=0
			str_tmp="$str"
			str1=""
			while [[ $count -lt 3 ]] 
			do
				if [[ $count -eq 0 ]] ; then
					days=$((j/5))
				elif [[ $count -eq 1 ]] ; then
					days=$j
				else 
					days=$((j*2))
				fi
				if [[ $days -lt 10 ]] ; then
					str="$str_tmp$threez$days$d"	
				elif [[ $days -lt 100 ]] ; then
					str="$str_tmp$twoz$days$d"
				elif [[ $days -lt 1000 ]] ; then
					str="$str_tmp$onez$days$d"
				else
					str="$str_tmp$days$d"
				fi
				str+="$i"
				str_c="$str"
				str+=".txt"
				if [[ $count -eq 0 ]] ; then
					str1="$str"
					python inputGenerator.py $str1
				else 
					fline="1s/.*/$j $w $days/"
					sed "$fline" $str1 > $str
				fi
				
				filename="test1.slurm"
				sline="2s/.*/#SBATCH -J $str_c/"
				tline="3s/.*/#SBATCH -o output_$str/"
				fourthline="4s/.*/#SBATCH -e errors_$str/"
				sed -i "$sline" $filename
				sed -i "$tline" $filename
				sed -i "$fourthline" $filename
				cpyt="5s/.*/str='$str'/"
				#modifico il file GG
				sed -i "$cpyt" GG.sh
				#./GG.sh
				sbatch test1.slurm
				
				echo $str
				sleep 20
				((count++))
			done
		done
	done
done
