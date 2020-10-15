#!/bin/bash

python monte_carlo.py --episodes 4000 --epsilon 0.3 --boxes 4 --render_each 4000 &
python monte_carlo.py --episodes 4000 --epsilon 0.3 --boxes 6 --render_each 4000 &
python monte_carlo.py --episodes 4000 --epsilon 0.3 --boxes 8 --render_each 4000 &
python monte_carlo.py --episodes 4000 --epsilon 0.3 --boxes 10 --render_each 4000 &
python monte_carlo.py --episodes 4000 --epsilon 0.3 --boxes 12 --render_each 4000 &
python monte_carlo.py --episodes 4000 --epsilon 0.3 --boxes 14 --render_each 4000 &
python monte_carlo.py --episodes 4000 --epsilon 0.3 --boxes 16 --render_each 4000 &
