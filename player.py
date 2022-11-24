#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
import math


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!

        children = initial_tree_node.compute_and_get_children()
        calculated_move = 0
        min_score = -math.inf


        for child in children:
            calculated_score = self.alphabeta(child , 2 ,-math.inf, math.inf,0 )
            if(min_score < calculated_score):
               min_score = calculated_score
               calculated_move = child.move
        return ACTION_TO_STR[calculated_move]

    def alphabeta(self, node, depth, alpha, beta, maximizingPlayer):
            if depth == 0 or list(node.state.get_fish_positions().keys()) == []:
                return self.calculate_heuristics(node, 0)


            else:
                if (maximizingPlayer == 0):
                    Value = -math.inf
                    for child in node.compute_and_get_children() :
                        Value = max(Value, self.alphabeta(child, depth-1, alpha, beta, 1))
                        alpha = max(alpha, Value)
                        if (beta <= alpha ): 
                            break # β cutoff

                else :
                    Value = math.inf
                    for child in node.compute_and_get_children() :
                        Value = min(Value,  self.alphabeta(child, depth-1, alpha, beta, 0))
                        beta = min(beta, Value)
                        if (beta <= alpha):
                            break # α cutoff 

                return Value

    def calculate_heuristics(self, node, player):
        state = node.state
        max_score, min_score = state.get_player_scores()
        heuristic = max_score - min_score
        
        hook_postion= state.hook_positions[player]
        fish_postions= state.fish_positions.values()
        
        heuristic = heuristic - self.get_dist_to_closest_fish(hook_postion,fish_postions)
        return heuristic

    def get_dist_to_closest_fish(self, hook_postion, fish_postions):
        distance = math.inf
        for fish_postion in fish_postions:
            distance = min(distance, self.get_dist_to_fish(hook_postion, fish_postion))
        return distance

    def get_dist_to_fish(self, hook_postion, fish_position):
        return math.sqrt((fish_position[0]-hook_postion[0])**2 + (fish_position[1]-hook_postion[1])**2)