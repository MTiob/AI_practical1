#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import copy

class Node:
    def __init__(self, score1, score2, player, string):
        self.score1 = score1 
        self.score2 = score2
        self.player = player
        self.string = string
        self.children = []
        
    def add_child(self, node):
        self.children.append(node)
        
    def generate_children(self):
        if len(self.string) <= 0:
            return
        
        for choice in [7, 5, 3, 2]:
            if choice not in self.string:
                continue
                
            for num in self.string:
                if num != choice:
                    continue
                        
                if self.player:
                    new_score1 = self.score1-num
                    new_score2 = self.score2
                    new_string = copy.deepcopy(self.string)
                    new_string.remove(num)
                    new_player = False
            
                else:
                    new_score1 = self.score1
                    new_score2 = self.score2-num
                    new_string = copy.deepcopy(self.string)
                    new_string.remove(num)
                    new_player = True
                        
                child = Node(new_score1, new_score2, new_player, new_string)
                
                if self.check_duplicate(child):
                    self.add_child(child)
                    if len(new_string) > 0:
                            child.generate_children()
                 
        return None

    
    def check_duplicate(self, node):
        for child in self.children:
            if node.string == child.string and node.score1 == child.score1 and node.score2 == child.score2:
                return False
        return True
                

                
                
class Tree:
    def __init__(self, score1, score2, string, turn_player1):
        self.root = Node(score1, score2, turn_player1, string)
        
    def generate_game_tree(self):
        self.root.generate_children()
            
    def AlphaBeta_search(self, node, alpha, beta):
        if not node.string:    
            #evaluation function
            if node.score1 < node.score2:
                value = -1
                return value
            elif node.score1 > node.score2:
                value = 1
                return value
            else:
                value = 0
                return value
            
        if node.player:
            
            #minimizing layer
            possible_minimum = 2
            
            for child in node.children:
                value = self.AlphaBeta_search(child, alpha, beta)
                if value < possible_minimum:
                    possible_minimum = value
                    if possible_minimum < beta:
                        beta = possible_minimum
                if beta <= alpha:
                    break
                    
            return possible_minimum
        
        else:
            #maximizing layer
            possible_maximum = -2
            
            for child in node.children:
                value = self.AlphaBeta_search(child, alpha, beta)
                if value > possible_maximum:
                    possible_maximum = value
                    if possible_maximum > alpha:
                        alpha = possible_maximum
                if alpha <= beta:
                    break
                    
            return possible_maximum

    def make_best_move(self, node):
        maximum = -2
        promise = None
        alpha = -2
        beta = 2
        for child in node.children:
            value = self.AlphaBeta_search(child, alpha, beta)
            if maximum < value:
                maximum = value
                promise = node.score2 - child.score2
                
        if promise != 0:
            return promise
        else:
            print("error")
            return


class game_concept:
    def __init__(self, turn_player1):
        self.score1 = 32 ###score for first player
        self.score2 = 32 ###score for second player
        self.string = [2,2,2,2,3,3,3,5,5,5,7,7] ###initial string 
        self.turn_player1 = turn_player1 ###flag for recognizing turn of game
        self.win = 0
        self.inp = 0
    
    def manip(self, choice):
        if self.turn_player1:
            self.inp = choice
                
            if self.inp == 2 or self.inp == 3 or self.inp == 5 or self.inp == 7:
                self.result = self.inp in self.string
                if self.result == True:
                    self.score1 = self.score1 - self.inp
                    self.string.remove(self.inp)
                    self.turn_player1 = False
                    return self.score1, self.score2, self.string, self.turn_player1
                elif self.result == False:
                    return
            else:
                return
                        
        else:
            tree = Tree(self.score1, self.score2, self.string, self.turn_player1)
            tree.generate_game_tree()
            self.inp = tree.make_best_move(tree.root)
                
            if self.inp == 2 or self.inp == 3 or self.inp == 5 or self.inp == 7:
                self.result = self.inp in self.string
                if self.result == True:
                    self.score2 = self.score2 - self.inp
                    self.string.remove(self.inp)
                    self.turn_player1 = True
                    return self.score1, self.score2, self.string, self.turn_player1
                elif self.result == False:
                    return
            else:
                return


    def check_v(self):
        # at the end of game, player who has less score wins the game
        if self.score1 < self.score2:
            self.win = 1
            return self.win
        
        elif self.score1 > self.score2:
            self.win = 2
            return self.win
        
        else:
            return self.win 
    
    def main(self, choice):
        if len(self.string) > 1:
            return self.manip(choice)
        
        else:
            self.manip(choice)
            if self.check_v() == 1:
                winner = "Player"
                return self.score1, self.score2, self.string, self.turn_player1, winner
            elif self.check_v() == 2:
                winner = "Computer"
                return self.score1, self.score2, self.string, self.turn_player1, winner
            else:
                winner = "Draw"
                return self.score1, self.score2, self.string, self.turn_player1, winner

