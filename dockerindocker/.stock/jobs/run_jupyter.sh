#!/bin/sh

mkdir -p /data/notebooks

/usr/local/bin/jupyter notebook --NotebookApp.notebook_dir='/data/notebooks'  --ip=0.0.0.0 \
    --allow-root >> /data/logs/jupyter-notebook.log
