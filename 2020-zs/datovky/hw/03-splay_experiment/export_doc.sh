#!/bin/bash

# export images

python export_plots.py
python export_log_plots.py


# export pdf
pandoc -t beamer -o splay_doc.pdf splay_doc.md


brave splay_doc.pdf
