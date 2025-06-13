import numpy as np
import matplotlib.pyplot as plt
import random as ra

def histogram(xs):
    fig, ax = plt.subplots()
    ax.hist(xs, bins = 100)
    average = np.mean(xs)
    ax.axvline(average, color='red')
    ylim = ax.get_ylim()[1]
    ax.text(average, ylim*0.9, f'Mean = {average}')
    #Someday, I'll be living in a big old city
    #And all you're ever gonna be is mean
    plt.show()

def main():
    avs = []
    for i in range(10000):
        draws = np.random.choice([0, 1], size=5000)
        average = np.mean(draws)
        avs.append(average)
    avs = np.array(avs)
    histogram(avs)

if __name__ == '__main__':
    main()