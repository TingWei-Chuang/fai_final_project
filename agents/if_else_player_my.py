from game.players import BasePokerPlayer
import random as rand
import numpy as np
from game.engine.hand_evaluator import HandEvaluator
from game.engine.card import Card
from collections import Counter


class IfElsePlayer(BasePokerPlayer):
    def __init__(self):
        self.hole = None
        self.community = None
        self.street = None

    def declare_action(self, valid_actions, hole_card, round_state):
        my_stack = self.find_stack(round_state["seats"], self.name)
        if my_stack - (self.max_round - round_state["round_count"] + 1) * self.small_blind * 1.5 >= self.initial_stack:
            return valid_actions[0]["action"], valid_actions[0]["amount"]
        
        evaluation = HandEvaluator.gen_hand_rank_info(self.hole, self.community)

        action_dict = dict()
        for act in valid_actions:
            action_dict[act["action"]] = act

        strength = evaluation["hand"]["strength"]

        if self.street == "preflop":
            if strength == "ONEPAIR":
                if evaluation["hand"]["high"] >= 6:
                    if action_dict["raise"]["amount"]["min"] > 0:
                        return "raise", min((action_dict["raise"]["amount"]["min"] + 10 * (evaluation["hand"]["high"] - 8), action_dict["raise"]["amount"]["max"]))
                return "call", action_dict["call"]["amount"]
            elif evaluation["hole"]["low"] >= 9:
                if action_dict["raise"]["amount"]["min"] > 0:
                    return "raise", min((action_dict["raise"]["amount"]["min"] + 10 * (evaluation["hand"]["low"] - 9), action_dict["raise"]["amount"]["max"]))
                return "call", action_dict["call"]["amount"]
            elif self.rank["hole"]["high"] >= 11:
                return "call", action_dict["call"]["amount"]
            else:
                if action_dict["call"]["amount"] < 30:
                    return "call", action_dict["call"]["amount"]
                else:
                    return "fold", action_dict["fold"]["fold"]
        elif self.street == "flop":
            if strength in ["STRAIGHTFLASH", "FOURCARD"]:
                if action_dict["raise"]["amount"]["min"] > 0:
                    return "raise", action_dict["raise"]["amount"]["max"]
                else:
                    return "call", action_dict["call"]["amount"]
            else:
                rank_counter = Counter()
                for card in self.community:
                    rank_counter[card.rank] += 1
                if self.hole[0].rank == self.hole[1].rank:
                    if self.hole[0].rank in rank_counter.keys():
                        if "raise" in action_dict.keys():
                            return "raise", (action_dict["raise"]["amount"]["min"] + action_dict["raise"]["amount"]["max"]) // 2
                        else:
                            return "call", action_dict["call"]["amount"]
                    else:
                        if action_dict["call"]["amount"] < 25:
                            return "call", action_dict["call"]["amount"]
                        else:
                            return "fold", action_dict["fold"]["amount"]
                else:
                    if self.hole[0].rank in rank_counter.keys() or self.hole[1].rank in rank_counter.keys():
                        if strength == "TWOPAIR" or strength == "THREECARD":
                            return "call", action_dict["call"]["amount"]
                        else:
                            if action_dict["call"]["amount"] < 25:
                                return "call", action_dict["call"]["amount"]
                            else:
                                return "fold", action_dict["fold"]["amount"]
                suit_counter = Counter()
                for card in self.community:
                    suit_counter[card.suit] += 1
                if self.hole[0].suit == self.hole[1].suit:
                    if self.hole[0].suit in suit_counter.keys():
                        if suit_counter[self.hole[0].suit] >= 2:
                            return "call", action_dict["call"]["amount"]
                        else:
                            if action_dict["call"]["amount"] < 50:
                                return "call", action_dict["call"]["amount"]
                            else:
                                return "fold", action_dict["fold"]["amount"]
                    else:
                        if action_dict["call"]["amount"] < 30:
                            return "call", action_dict["call"]["amount"]
                        else:
                            return "fold", action_dict["fold"]["amount"]
                else:
                    if self.hole[0].suit in suit_counter.keys():
                        if suit_counter[self.hole[0].suit] >= 3:
                            return "call", action_dict["call"]["amount"]
                        else:
                            if action_dict["call"]["amount"] < 30:
                                return "call", action_dict["call"]["amount"]
                            else:
                                return "fold", action_dict["fold"]["amount"]
                    elif self.hole[1].suit in suit_counter.keys():
                        if suit_counter[self.hole[1].suit] >= 3:
                            return "call", action_dict["call"]["amount"]
                        else:
                            if action_dict["call"]["amount"] < 30:
                                return "call", action_dict["call"]["amount"]
                            else:
                                return "fold", action_dict["fold"]["amount"]
                if action_dict["call"]["amount"] < 20:
                    return "call", action_dict["call"]["amount"]
                else:
                    return "fold", action_dict["fold"]["amount"]
        elif self.street == "turn":
            if strength == "STRAIGHTFLASH" or strength == "FOURCARD":# or strength == "FULLHOUSE" or strength == "FLASH":
                if "raise" in action_dict.keys():
                    return "raise", action_dict["raise"]["amount"]["max"]
                else:
                    return "call", action_dict["call"]["amount"]
            else:
                rank_counter = Counter()
                for card in self.community:
                    rank_counter[card.rank] += 1
                if self.hole[0].rank == self.hole[1].rank:
                    if self.hole[0].rank in rank_counter.keys():
                        if "raise" in action_dict.keys():
                            return "raise", (action_dict["raise"]["amount"]["min"] + action_dict["raise"]["amount"]["max"]) // 2
                        else:
                            return "call", action_dict["call"]["amount"]
                    else:
                        if action_dict["call"]["amount"] < 25:
                            return "call", action_dict["call"]["amount"]
                        else:
                            return "fold", action_dict["fold"]["amount"]
                else:
                    if self.hole[0].rank in rank_counter.keys() or self.hole[1].rank in rank_counter.keys():
                        if strength == "TWOPAIR" or strength == "THREECARD":
                            return "call", action_dict["call"]["amount"]
                        else:
                            if action_dict["call"]["amount"] < 25:
                                return "call", action_dict["call"]["amount"]
                            else:
                                return "fold", action_dict["fold"]["amount"]
                suit_counter = Counter()
                for card in self.community:
                    suit_counter[card.suit] += 1
                if self.hole[0].suit == self.hole[1].suit:
                    if self.hole[0].suit in suit_counter.keys():
                        if suit_counter[self.hole[0].suit] >= 2:
                            return "call", action_dict["call"]["amount"]
                        else:
                            if action_dict["call"]["amount"] < 50:
                                return "call", action_dict["call"]["amount"]
                            else:
                                return "fold", action_dict["fold"]["amount"]
                    else:
                        if action_dict["call"]["amount"] < 30:
                            return "call", action_dict["call"]["amount"]
                        else:
                            return "fold", action_dict["fold"]["amount"]
                else:
                    if self.hole[0].suit in suit_counter.keys():
                        if suit_counter[self.hole[0].suit] >= 3:
                            return "call", action_dict["call"]["amount"]
                        else:
                            if action_dict["call"]["amount"] < 30:
                                return "call", action_dict["call"]["amount"]
                            else:
                                return "fold", action_dict["fold"]["amount"]
                    elif self.hole[1].suit in suit_counter.keys():
                        if suit_counter[self.hole[1].suit] >= 3:
                            return "call", action_dict["call"]["amount"]
                        else:
                            if action_dict["call"]["amount"] < 30:
                                return "call", action_dict["call"]["amount"]
                            else:
                                return "fold", action_dict["fold"]["amount"]
                if action_dict["call"]["amount"] < 20:
                    return "call", action_dict["call"]["amount"]
                else:
                    return "fold", action_dict["fold"]["amount"]
        elif self.street == "river":
            if strength == "STRAIGHTFLASH" or strength == "FOURCARD":# or strength == "FULLHOUSE" or strength == "FLASH":
                if "raise" in action_dict.keys():
                    return "raise", action_dict["raise"]["amount"]["max"]
                else:
                    return "call", action_dict["call"]["amount"]
            else:
                rank_counter = Counter()
                for card in self.community:
                    rank_counter[card.rank] += 1
                if self.hole[0].rank == self.hole[1].rank:
                    if self.hole[0].rank in rank_counter.keys():
                        if "raise" in action_dict.keys():
                            return "raise", (action_dict["raise"]["amount"]["min"] + action_dict["raise"]["amount"]["max"]) // 2
                        else:
                            return "call", action_dict["call"]["amount"]
                    else:
                        if action_dict["call"]["amount"] < 25:
                            return "call", action_dict["call"]["amount"]
                        else:
                            return "fold", action_dict["fold"]["amount"]
                else:
                    if self.hole[0].rank in rank_counter.keys() or self.hole[1].rank in rank_counter.keys():
                        if strength == "TWOPAIR" or strength == "THREECARD":
                            return "call", action_dict["call"]["amount"]
                        else:
                            if action_dict["call"]["amount"] < 25:
                                return "call", action_dict["call"]["amount"]
                            else:
                                return "fold", action_dict["fold"]["amount"]
                suit_counter = Counter()
                for card in self.community:
                    suit_counter[card.suit] += 1
                if self.hole[0].suit == self.hole[1].suit:
                    if self.hole[0].suit in suit_counter.keys():
                        if suit_counter[self.hole[0].suit] >= 2:
                            return "call", action_dict["call"]["amount"]
                        else:
                            if action_dict["call"]["amount"] < 50:
                                return "call", action_dict["call"]["amount"]
                            else:
                                return "fold", action_dict["fold"]["amount"]
                    else:
                        if action_dict["call"]["amount"] < 30:
                            return "call", action_dict["call"]["amount"]
                        else:
                            return "fold", action_dict["fold"]["amount"]
                else:
                    if self.hole[0].suit in suit_counter.keys():
                        if suit_counter[self.hole[0].suit] >= 3:
                            return "call", action_dict["call"]["amount"]
                        else:
                            if action_dict["call"]["amount"] < 30:
                                return "call", action_dict["call"]["amount"]
                            else:
                                return "fold", action_dict["fold"]["amount"]
                    elif self.hole[1].suit in suit_counter.keys():
                        if suit_counter[self.hole[1].suit] >= 3:
                            return "call", action_dict["call"]["amount"]
                        else:
                            if action_dict["call"]["amount"] < 30:
                                return "call", action_dict["call"]["amount"]
                            else:
                                return "fold", action_dict["fold"]["amount"]
                if action_dict["call"]["amount"] < 20:
                    return "call", action_dict["call"]["amount"]
                else:
                    return "fold", action_dict["fold"]["amount"]
                

        if "call" in action_dict.keys():
            return "call", action_dict["call"]["amount"]
        return "fold", action_dict["fold"]["amount"]

    def receive_game_start_message(self, game_info):
        self.max_round = game_info["rule"]["max_round"]
        self.initial_stack = game_info["rule"]["initial_stack"]
        self.small_blind = game_info["rule"]["small_blind_amount"]
        self.name = self.find_name(game_info["seats"], self.uuid)
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.hole = [Card.from_str(card) for card in hole_card]
        pass

    def receive_street_start_message(self, street, round_state):
        self.street = street
        self.community = [Card.from_str(card) for card in round_state["community_card"]]

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

    def find_stack(self, seats, name):
        for s in seats:
            if s["name"] == name:
                return s["stack"]
            
    def find_name(self, seats, uuid):
        for s in seats:
            if s["uuid"] == uuid:
                return s["name"]


def setup_ai():
    p = IfElsePlayer()
    return p
