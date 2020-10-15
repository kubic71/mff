#!/bin/bash

python monte_carlo.py --episodes 2000 --epsilon 0.4 --boxes 8 --render_each 4000 &
python monte_carlo.py --episodes 2000 --epsilon 0.3 --boxes 8 --render_each 4000 &
python monte_carlo.py --episodes 2000 --epsilon 0.2 --boxes 8 --render_each 4000 &
python monte_carlo.py --episodes 2000 --epsilon 0.15 --boxes 8 --render_each 4000 &
python monte_carlo.py --episodes 2000 --epsilon 0.1 --boxes 8 --render_each 4000 &
python monte_carlo.py --episodes 2000 --epsilon 0.075 --boxes 8 --render_each 4000 &
python monte_carlo.py --episodes 2000 --epsilon 0.05 --boxes 8 --render_each 4000 &
python monte_carlo.py --episodes 2000 --epsilon 0.03 --boxes 8 --render_each 4000 &

