#!/bin/bash

ROSETTA=/opt/rosetta_3.13/main/source  # Rosetta source path
source /opt/pip-env/bin/activate  # activate python environment
SCRIPTS=/workspace/Rosetta/scripts  # RosettaCode/scripts path

for P in input_ligand/*.sdf; do
    python3 ${SCRIPTS}/sdf_split.py $P -n 1
    for P2 in ${P%.*}_*.sdf; do
        PA=${P2%.*}
        python3 ${ROSETTA}/scripts/python/public/molfile_to_params.py ${P2} \
            -p ligand_chain_X \
            --mm-as-virt \
            --chain X \
            --clobber
        # リガンド中心の座標が欲しい場合↓
        # python3 ${SCRIPTS}/center.py ${P2} (center.py参照)
        
        cat input_protein/protein.pdb ligand_chain_X_0001.pdb > dock.pdb
        mpirun -np 50 --allow-run-as-root ${ROSETTA}/bin/rosetta_scripts.mpi.linuxgccrelease \
            -s dock.pdb \
            -extra_res_fa ligand_chain_X.params \
            -out:file:scorefile output/${PA##*/}.sc \
            -out:pdb true \
            -out:prefix output_dock/${PA##*/}_ \
            -packing:ex1 \
            -packing:ex2 \
            -packing:no_optH \
            -packing:flip_HNQ \
            -parser:protocol dock.xml \
            -overwrite \
            -mistakes:restore_pre_talaris_2013_behavior true \
            -nstruct 50 \
            -score:analytic_etable_evaluation true 
        rm ligand_chain_X.*
        rm $P2
    done
done

bash ${SCRIPTS}sc_parser.sh output
python3 ${SCRIPTS}/select_score.py \
    --score_path "output" \
    --criteria "interface" \
    --number 10


for P in output_dock/*.pdb; do
    PA=${P%.*}
    python3 ${SCRIPTS}/extract_ligand.py $P --remove_chain
    python3 ${ROSETTA}/scripts/python/public/molfile_to_params.py ligand_chain_X.sdf \
        -p ligand_chain_X \
        --mm-as-virt \
        --chain X \
        --clobber
    cat protein.pdb ligand_chain_X_0001.pdb > dock.pdb
    mpirun -np 50 --allow-run-as-root ${ROSETTA}/bin/rosetta_scripts.mpi.linuxgccrelease \
        -s dock.pdb \
        -extra_res_fa ligand_chain_X.params \
        -out:file:scorefile output2/${PA##*/}.sc \
        -out:pdb true \
        -out:prefix output_dock2/${PA##*/}_ \
        -packing:ex1 \
        -packing:ex2 \
        -packing:no_optH \
        -packing:flip_HNQ \
        -parser:protocol dock2.xml \
        -overwrite \
        -mistakes:restore_pre_talaris_2013_behavior true \
        -nstruct 50 \
        -score:analytic_etable_evaluation true 
done

bash ${SCRIPTS}/sc_parser.sh output2