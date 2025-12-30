#FROM --platform=linux/amd64 jupyter/pytorch-notebook
FROM --platform=linux/amd64 quay.io/jupyter/pytorch-notebook

#USER $NB_UID
USER root

RUN	sudo apt -y update && \
	sudo apt -y upgrade && \
	sudo apt install -y apt-utils graphviz libzmq3-dev && \
	sudo apt install -y  build-essential gfortran unzip wget libblas-dev liblapack-dev pkg-config libmetis-dev patch &&\
	sudo apt install -y libpng-dev libfreetype6-dev git 

RUN conda install conda-forge::ipopt
RUN conda install -y conda-forge::cyipopt 
RUN conda install -y conda-forge::pyoptsparse
# RUN conda install conda-forge ipopt glpk

RUN	pip install --upgrade pip && \
  	pip install control drake jax osqp meshcat pyomo manipulation underactuated ipyopt && \
        fix-permissions "/home/${NB_USER}"
