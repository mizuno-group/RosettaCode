FROM python:3.11-slim-bullseye

WORKDIR /workspace

RUN apt update && \
    apt install -y tzdata

ENV TZ=Asia/Tokyo

RUN apt update \
    && apt install -y \
    curl \
    vim \
    less \
    git \
    nodejs \
    npm \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt install -y locales \
    && locale-gen ja_JP.UTF-8 \
    && echo "export LANG=ja_JP.UTF-8" >> ~/.bashrc

RUN cd /opt && \
    wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    /bin/bash /opt/Miniconda3-latest-Linux-x86_64.sh -b -p "/opt/miniconda3" && \
    rm /opt/Miniconda3-latest-Linux-x86_64.sh && \
    export PATH=/opt/miniconda3/bin:$PATH && \
    echo ". /opt/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc && \
    ln -s /opt/miniconda3/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo "conda activate" >> ~/.bashrc && \
    . /opt/miniconda3/etc/profile.d/conda.sh && \
    conda activate && \
    conda update conda && \
    conda create -y -n rosetta-env python=3.9 libffi=3.3 && \
    conda activate rosetta-env && \
    conda install pip && \
    pip install setuptools jupyter flake8 autopep8 && \
    pip install rdkit pandas scipy optuna plotly scikit-learn tqdm matplotlib pubchempy xgboost lightgbm && \
    git clone https://github.com/openbabel/openbabel.git && \
    apt install -y libxml2-dev libboost-all-dev libomp-dev zlib1g-dev libeigen3-dev libcairo2-dev cmake swig && \
    cd openbabel && \
    mkdir build && cd build && \
    cmake -DENABLE_OPENMP=ON -DBUILD_GUI=OFF -DPYTHON_EXECUTABLE=${HOME}/miniconca3/envs/pip-env/bin/python3 -DPYTHON_BINDINGS=ON -DRUN_SWIG=ON .. && \
    make -j 33 && \
    make install && \
    pip install plip && \
    rm -rf /var/lib/apt/lists/*

RUN cd /opt && \
    apt update && \
    apt install -y gfortran && \
    wget https://www.open-mpi.org/software/ompi/v4.1/downloads/openmpi-4.1.4.tar.gz --no-check-certificate && \
    tar -zxvf openmpi-4.1.4.tar.gz && \
    cd openmpi-4.1.4 && \
    ./configure --prefix=/usr/local/openmpi-4.1.4 CC=gcc CXX=g++ && \
    make -j 16 all 2>&1 | tee make.log && \
    make -j 16 install 2>&1 | tee install.log

ENV MPIROOT=/usr/local/openmpi-4.1.4 \
    LD_LIBRARY_PATH=/opt/openbabel/build/lib:${MPIROOT}/lib:${LD_LIBRARY_PATH} \
    PATH=/opt/openbabel/build/bin:${MPIROOT}/bin:${PATH}

# Rosetta installation
COPY rosetta_bin_linux_3.13_bundle.tgz /opt/ 
COPY bcl-4.3.0-Linux-x86_64.sh /opt/

RUN apt update && \
    cd /opt && \
    tar -zxvf rosetta_bin_linux_3.13_bundle.tgz && \
    mv rosetta_bin_linux_2021.16.61629_bundle rosetta_3.13 && \
    cd /opt/rosetta_3.13/main/source && \
    CC=gcc CXX=g++ ./scons.py -j16 mode=release bin && \
    CC=gcc CXX=g++ ./scons.py -j16 bin mode=release extras=mpi && \
    apt install -y freeglut3-dev gcc tcl8.6-dev tk8.6-dev libmsgpack-dev libpng-dev libfreetype6-dev libglm-dev libglew-dev python3-pyqt5.qtopengl python3-pip libxml2-dev libnetcdf-dev && \
    cd /opt && \
    git clone https://github.com/schrodinger/pymol-open-source.git && \
    git clone https://github.com/rcsb/mmtf-cpp.git && \
    mv mmtf-cpp/include/mmtf* pymol-open-source/include/ && \
    rm -r mmtf-cpp && \
    cd pymol-open-source && \
    export CPPFLAGS="-std=c++0x" && \
    python3 setup.py build install --home=/opt/pymol-open-source-build --install-lib=/opt/pymol-open-source/modules --install-scripts=/opt/pymol-open-source-build && \
    cd /opt && \
    echo y | bash bcl-4.3.0-Linux-x86_64.sh && \
    rm -rf /var/lib/apt/lists/* && \
    rm /opt/*gz

COPY bcl.license /opt/bcl-4.3.0-Linux-x86_64/

ENV PYTHONPATH /opt/pymol-open-source/modules:${PYTHONPATH} \
    PATH /opt/rosetta_3.13/main/source/bin:${PATH}
     