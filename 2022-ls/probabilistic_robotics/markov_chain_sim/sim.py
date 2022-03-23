"""Markov chain simulation"""
from typing import List
import numpy as np
import pandas as pd


### States
SUNNY = 0
CLOUDY = 1
RAINY = 2


trainsition_prob = np.array([
    [0.8, 0.2, 0], # sunny
    [0.4, 0.4, 0.2], # cloudy
    [0.2, 0.6, 0.2]  # rainy
])

initial_state = 0


def markov_chain(P: np.ndarray, s, t: int) -> np.ndarray:
    """
    Markov chain simulation
    Arguments:
    - P: transition probability matrix
    - s: initial state
    - t: number of iterations
    Return:
    - states: simulated states
    """

    # state can be either index of the state or a initial probability distribution over states

    if isinstance(s, int):
        state = np.zeros(P.shape[0])
        state[s] = 1
        state = np.array([state])

    else:
        state = s

    # state.shape = (1, 3)
    # P.shape = (3, 3)

    # next_state = state @ P

    for i in range(t):
        state = state @ P
        print(state)

    return state

def print_weather(weather: np.ndarray):

    print("Sunny:", weather[0, SUNNY])
    print("Cloudy:", weather[0, CLOUDY])
    print("Rainy:", weather[0, RAINY])

# Monday is sunny
# What's the weather on Thursday?
weather = markov_chain(trainsition_prob, SUNNY, 3)

# Print the weather on Thursday
print("Weather on Thursday:")
print_weather(weather)


def probability_of_a_sequence(P: np.ndarray, state_seq: List[int]):
    """
    Probability of a sequence
    Arguments:
    - P: transition probability matrix
    - state_seq: sequence of states
    Return:
    - prob: probability of the sequence
    """

    prob = 1
    for i in range(len(state_seq) - 1):
        prob *= P[state_seq[i], state_seq[i + 1]]
    return prob

# Given that it's sunny on Monday, what's the probability of a sequence
# Tuesday - cloudy
# Wednesday - cloudy
# Thursday - rainy
#
# P(T0 = sunny, T1 = cloudy, T2 = cloudy, T3 = rainy)

print("\nProbability of a sequence:")
print("P(T0 = sunny, T1 = cloudy, T2 = cloudy, T3 = rainy) =", probability_of_a_sequence(trainsition_prob, [SUNNY, CLOUDY, CLOUDY, RAINY]))


path = []


# show the evolution for multiple different initial states
n_initial = 500


states = np.random.rand(n_initial, 3)
for i in range(n_initial):
    # normalize
    states[i] = states[i] / np.sum(states[i])

path = [states]

TIMESTEPS = 10
for i in range(TIMESTEPS-1):
    path.append(markov_chain(trainsition_prob, states, i))
    print(path[-1])


data = pd.DataFrame(columns=['x', 'y', 'z', 'time', 'path_id'])

for i in range(n_initial):
    for t in range(TIMESTEPS):
        data.loc[len(data)] = [path[t][i, 0], path[t][i, 1], path[t][i, 2], t, i]


# eigen-vectors
eigen_vectors = np.linalg.eig(trainsition_prob.transpose())[1]
eigen_values = np.linalg.eig(trainsition_prob.transpose())[0]

print("\nEigen vectors:")
print(eigen_vectors)
print("\nEigen values:")
print(eigen_values)

stationary_dist = eigen_vectors[:, 0] / np.sum(eigen_vectors[:, 0])

print("\nStationary distribution:")
print(stationary_dist)

def plot_3d_plotly(data: pd.DataFrame, stationary_dist: np.ndarray):
    import plotly.express as px 
    import plotly.graph_objects as go

    fig = px.scatter_3d(data, x='x', y='y', z='z', color='time')

    fig.add_trace(
        go.Scatter3d(
            x=[stationary_dist[0]],
            y=[stationary_dist[1]],
            z=[stationary_dist[2]],
            mode='markers',
            marker=dict(
                size=12,
                symbol='x',
                color='rgb(255, 0, 0)',
                line=dict(
                    color='rgb(204, 204, 204)',
                    width=1
                )
            )
        )
    )



    fig.show()


plot_3d_plotly(data, stationary_dist)



def plot_2d(paths: List[np.ndarray], stationary_dist: np.ndarray):
    import matplotlib.pyplot as plt
    import seaborn as sns

    paths = np.array(paths)

    # paths.shape = (TIMESTEPS, n_paths, 3)

    timesteps = paths.shape[0]
    n_paths = paths.shape[1]

    colormap = plt.cm.gist_ncar

    # make the color change with time

    for i in range(n_paths):
        x = paths[:, i, 0]
        y = paths[:, i, 1]
        # sns.lineplot(x=x, y=y, color='black')


    for t in range(timesteps):
        points = paths[t]

        x = points[:, 0]
        y = points[:, 1]
        color = colormap(t/(timesteps+1))
        
        sns.scatterplot(x=x, y=y, color=color)

    # plot eigen values
    # plt.scatter(0, 0, c='black', s=100)

    plt.scatter(x=[stationary_dist[0]], y=[stationary_dist[1]], c='black', s=100)

    plt.show()



def plot_3d(paths: List[np.ndarray], stationary_dist: np.ndarray):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    paths = np.array(paths)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # paths.shape = (TIMESTEPS, n_paths, 3)

    timesteps = paths.shape[0]
    n_paths = paths.shape[1]

    for i in range(n_paths):
        x = paths[:, i, 0]
        y = paths[:, i, 1]
        z = paths[:, i, 2]
        ax.plot(x, y, z)

    colormap = plt.cm.gist_ncar
    for t in range(timesteps):
        points = paths[t]
        color = colormap(t/(timesteps+1))

        x = points[:, 0]
        y = points[:, 1]
        z = points[:, 2]

        ax.scatter(x, y, z, color=color)

    # plot eigen values
    # plt.scatter(0, 0, c='black', s=100)

    ax.scatter(xs=[stationary_dist[0]], ys=[stationary_dist[1]], zs=[stationary_dist[2]], c='black', s=100)


    plt.show()





# plot_3d(path, stationary_dist)
# plot_2d(path, stationary_dist)



# def plot_3d(paths: List[List[np.ndarray]]):
#     # plot a path in 3D
#     from mpl_toolkits.mplot3d import Axes3D
#     import matplotlib.pyplot as plt
# 
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
# 
#     for path in paths:
#         for point in path:
#             pass
# 
# 
# 
#     ax.set_xlabel("Sunny")
#     ax.set_ylabel("Cloudy")
#     ax.set_zlabel("Rainy")
#     plt.show()
