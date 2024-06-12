from game.players import BasePokerPlayer
import random as rand
import numpy as np
from game.engine.hand_evaluator import HandEvaluator
from game.engine.card import Card
from collections import Counter
import random


class SampleBravePlayer(BasePokerPlayer):
    def __init__(self):
        self.hole = None
        self.community = None
        self.street = None
        self.n_sample = 30000
        self.possible_cards = None
        self.max_round = 0
        self.initial_stack = 0
        self.small_blind = 0
        self.RANK = list("23456789TJQKA")
        self.SUIT = list("CDHS")

    def find_stack(self, seats, name):
        for s in seats:
            if s["name"] == name:
                return s["stack"]

    def declare_action(self, valid_actions, hole_card, round_state):
        my_stack = self.find_stack(round_state["seats"], self.name)
        if my_stack - (self.max_round - round_state["round_count"] + 1) * self.small_blind * 1.5 >= self.initial_stack:
            return valid_actions[0]["action"], valid_actions[0]["amount"]
        wins = 0
        win_rate = 0.
        if self.street == "preflop":
            for i in range(self.n_sample):
                cards = list(np.random.choice(self.possible_cards, 7, replace=False))
                opponent_cards = cards[:2]
                community_cards = cards[2:]
                opponent_score = HandEvaluator.eval_hand(opponent_cards, community_cards)
                my_score = HandEvaluator.eval_hand(self.hole, community_cards)
                if my_score >= opponent_score:
                    wins += 1
            win_rate = wins / self.n_sample
        elif self.street == "flop":
            for i in range(self.n_sample):
                cards = list(np.random.choice(self.possible_cards, 4, replace=False))
                opponent_cards = cards[:2]
                community_cards = cards[2:]
                opponent_score = HandEvaluator.eval_hand(opponent_cards, self.community + community_cards)
                my_score = HandEvaluator.eval_hand(self.hole, self.community + community_cards)
                if my_score >= opponent_score:
                    wins += 1
            win_rate = wins / self.n_sample
        elif self.street == "turn":
            for i in range(self.n_sample):
                cards = list(np.random.choice(self.possible_cards, 3, replace=False))
                opponent_cards = cards[:2]
                community_cards = cards[2:]
                opponent_score = HandEvaluator.eval_hand(opponent_cards, self.community + community_cards)
                my_score = HandEvaluator.eval_hand(self.hole, self.community + community_cards)
                if my_score >= opponent_score:
                    wins += 1
            win_rate = wins / self.n_sample
        else:
            for i in range(self.n_sample):
                cards = list(np.random.choice(self.possible_cards, 2, replace=False))
                opponent_cards = cards[:2]
                community_cards = cards[2:]
                opponent_score = HandEvaluator.eval_hand(opponent_cards, self.community)
                my_score = HandEvaluator.eval_hand(self.hole, self.community)
                if my_score >= opponent_score:
                    wins += 1
            win_rate = wins / self.n_sample

        action_dict = dict()
        for act in valid_actions:
            action_dict[act["action"]] = act

        if win_rate >= 0.5:
            if action_dict["raise"]["amount"]["min"] > 0:
                r = (win_rate - 0.5) / 0.5
                return "raise", int((action_dict["raise"]["amount"]["min"]) * (1 - r) + (action_dict["raise"]["amount"]["max"]) * r)
            return "call", action_dict["call"]["amount"]
        if win_rate >= 0.4:
            if action_dict["call"]["amount"] < 30:
                return "call", action_dict["call"]["amount"]
            return "fold", action_dict["fold"]["amount"]
        else:
            if action_dict["call"]["amount"] < 15:
                return "call", action_dict["call"]["amount"]
            return "fold", action_dict["fold"]["amount"]


    def find_name(self, seats, uuid):
        for s in seats:
            if s["uuid"] == uuid:
                return s["name"]


    def receive_game_start_message(self, game_info):
        #print("receive_game_start_message")
        self.max_round = game_info["rule"]["max_round"]
        self.initial_stack = game_info["rule"]["initial_stack"]
        self.small_blind = game_info["rule"]["small_blind_amount"]
        self.name = self.find_name(game_info["seats"], self.uuid)
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        #print("receive_round_start_message")
        self.hole = [Card.from_str(card) for card in hole_card]
        pass

    def receive_street_start_message(self, street, round_state):
        #print("receive_street_start_message")
        self.street = street
        self.community = [Card.from_str(card) for card in round_state["community_card"]]
        self.possible_cards = self.__generate_possible_cards_without(self.hole + self.community)

    def __generate_possible_cards_without(self, without: list):
        possible_cards = []
        for r in self.RANK:
            for s in self.SUIT:
                card_raw = s + r
                possible_cards.append(Card.from_str(card_raw))
        selected_cards = []
        for card in possible_cards:
            if not card in without:
                selected_cards.append(card)
        return selected_cards

    def receive_game_update_message(self, new_action, round_state):
        #print("receive_game_update_message")
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        #print("receive_round_result_message")
        pass


def setup_ai():
    p = SampleBravePlayer()
    return p
