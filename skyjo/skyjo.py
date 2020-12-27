import numpy as np

cards = [ [-2] * 5, [-1] * 10, [0] * 15 , [1] * 10 , [2] * 10 , [3] * 10 , [4] * 10 , [5] * 10 , [6] * 10 ,
          [7] * 10 , [8] * 10 , [9] * 10 , [10] * 10 , [11] * 10 , [12] * 10]
cards = [item for sublist in cards for item in sublist]


class Skyjo:

    def __init__(self):
        self.values = np.random.choice(cards, 12)
        self.states = [False] * 12

    def play(self):
        print(s.states)
        print(s.values)



if __name__ == '__main__':

    s = Skyjo()
    s.play()