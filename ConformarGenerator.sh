#!/bin/bash

BCLCONF=/opt/bcl-4.3.0-Linux-x86_64
source /opt/pip-env/bin/activate


# conformer generation is conducted by separated script
files=()
i=0
for S in input_ligand/*.sdf; do
    if [ ! -f ${S%.*}_conf.sdf ]; then
	      files[${i}]=$S
	      i+=1
    fi
done

for S in "${files[@]}"; do
    ${BCLCONF}/bcl.exe molecule:ConformerGenerator \
        -license_file ${BCLCONF}/bcl.license \
        -add_h \
        -max_iterations 8000 \
        -top_models 100 \
        -ensemble_filenames $S \
        -conformers_single_file ${S%.*}_conf.sdf 
done
