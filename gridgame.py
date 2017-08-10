from random import randint,random,choice
from copy import deepcopy
from math import log
from genetic_program1 import *
import operator
from board import Board
from time import sleep
import threading
from numpy import array

training = True
def gridgame(p):
    global board, training
    #Board size
    max = (3,3)

    #Remember the last move for each player
    lastmove = [-1, -1]

    #Remember the players' locations from beginning
    location = [[randint(0, max[0]), randint(0, max[1])],]

    #Put the second player a sufficient distance from first
    location.append([(location[0][0]+2)%4, (location[0][1]+2)%4])
    if not training:
        board.move(0, array(location[0]))
        board.move(1, array(location[1]))
    
    #Maximum of 50 moves before a tie
    for o in range(50):
        #For each player
        for i in range(2):
            locs = location[i][:]+location[1-i][:]
            locs.append(lastmove[i])
            move = p[i].evaluate(locs)%4
            #You lose if you move the same direction twice
            
            if lastmove[i] == move:
                #print("winner is ", 1-i)
                return 1-i
            lastmove[i] = move
            #Changing the location of the current player
            if move == 0:
                location[i][0]-=1
                #Board limits
                if location[i][0]<0:
                    location[i][0]=0
            if move == 1:
                location[i][0]+=1
                if location[i][0]>max[0]:
                    location[i][0]= max[0]
            if move == 2:
                location[i][1]-=1
                if location[i][1]<0:
                    location[i][1]=0
            if move == 3:
                location[i][1]+=1
                if location[i][1]>max[1]:
                    location[i][1]=max[1]
            #If you have captured other player, you win.
            if not training:
                board.move(i, array(location[i]))
            if location[i] == location[i-1]:
                #print("Winner is ",i)
                return i
    #print("Game Draw")
    return -1


def tournament(pl):
    #Count losses
    losses=[0 for p in pl]
    #Every player plays every other player
    for i in range(len(pl)):
        for j in range(len(pl)):
            if i==j: continue

            #Who is the winner:
            winner = gridgame([pl[i], pl[j]])

            #Two points for a loss, one for tie
            if winner == 0:
                losses[j]+=2
            elif winner == 1:
                losses[i]+=2
            elif winner == -1:
                losses[i]+=1
                losses[j]+=1
                pass
    #Sort and return results
    pairs={}
    for _ in range(len(losses)):
        pairs[pl[_]] = losses[_]
    z=[]
    for key,value in sorted(pairs.items(),key=operator.itemgetter(1),reverse=False):
        z.append((value, key))
    return z

winner =None
def begin():
    global winner
    winner=evolve(5,100,tournament,maxgen=10)
    print(winner)


board = Board()
threading.Thread(target = begin).start()
board.root.mainloop()



class humanplayer:

    def evaluate(self, board):

        #get my location and the location of other players
        me = tuple(board[0:2])
        others = [tuple(board[x:x+2]) for x in range(2, len(board)-1, 2)]

        #Display the board
        for i in range(4):
            for j in range(4):
                if (i, j) == me:
                    print('0',end="")
                elif (i, j) in others:
                    print('X')
                else:
                    print(".",end="")
            print("\n")

        #Show moves, for reference
        print("Your last move was {}".format(board[len(board)-1]))
        print(' 0')
        print('2 3')
        print('1')
        print('Enter move: ',end="")
        #Return whatever user enters
        move = int(input())
        return move


training = False
def play():
    gridgame([winner,humanplayer( )])


board = Board();threading.Thread(target = play).start();board.root.mainloop()        


"""
Best program tree till now:

add
 p4
 add
  if
   sqroot
    subtract
     add
      6
      multiply
       square
        isgreater
         8
         multiply
          isgreater
           sqroot
            10
           add
            p3
            2
          sqroot
           if
            2
            p2
            0
       sqroot
        add
         square
          add
           5
           p1
         square
          10
     3
   isgreater
    square
     if
      sqroot
       7
      1
      add
       isgreater
        add
         square
          subtract
           6
           sqroot
            2
         if
          isgreater
           p1
           add
            1
            p4
          if
           p1
           add
            5
            7
           sqroot
            2
          8
        add
         multiply
          add
           if
            p2
            8
            1
           isgreater
            3
            10
          subtract
           sqroot
            9
           isgreater
            10
            4
         1
       add
        if
         if
          isgreater
           if
            10
            2
            2
           8
          if
           sqroot
            p0
           4
           sqroot
            0
          if
           sqroot
            9
           6
           subtract
            p0
            5
         subtract
          add
           multiply
            0
            8
           if
            0
            3
            5
          multiply
           multiply
            p1
            p2
           subtract
            4
            p3
         sqroot
          p2
        6
    if
     0
     subtract
      if
       p2
       isgreater
        subtract
         sqroot
          if
           add
            10
            3
           sqroot
            4
           sqroot
            9
         square
          if
           add
            2
            2
           p2
           subtract
            p2
            6
        sqroot
         sqroot
          if
           7
           multiply
            4
            7
           square
            p0
       if
        sqroot
         square
          add
           7
           6
        subtract
         6
         multiply
          if
           sqroot
            if
             2
             p4
             multiply
              10
              square
               isgreater
                sqroot
                 p4
                square
                 p4
           if
            sqroot
             sqroot
              subtract
               8
               sqroot
                multiply
                 square
                  if
                   10
                   5
                   p0
                 2
            isgreater
             3
             p3
            subtract
             add
              subtract
               multiply
                8
                p4
               9
              multiply
               sqroot
                9
               9
             p0
           multiply
            sqroot
             9
            6
          square
           add
            sqroot
             square
              square
               6
            square
             3
        square
         10
      add
       subtract
        subtract
         isgreater
          4
          2
         4
        9
       p3
     3
   if
    6
    subtract
     5
     3
    if
     subtract
      10
      square
       isgreater
        multiply
         4
         sqroot
          square
           3
        3
     3
     5
  subtract
   square
    if
     p4
     6
     9
   if
    6
    subtract
     5
     3
    if
     subtract
      add
       p2
       3
      square
       square
        subtract
         if
          add
           p2
           0
          isgreater
           square
            p3
           8
          0
         sqroot
          sqroot
           7
     3
     5"""
