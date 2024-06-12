from game.players import BasePokerPlayer
from game.engine.hand_evaluator import HandEvaluator
from game.engine.card import Card

class AgentPlayer(
    BasePokerPlayer
):  # Do not forget to make parent class as "BasePokerPlayer"
    def find_stack(self, seats, name):
        for seat in seats:
            if seat["name"] == name:
                return seat["stack"]
    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state):
        my_stack = self.find_stack(round_state["seats"], self.name)
        if my_stack - (self.max_round - round_state['round_count'] + 1) * self.small_blind * 1.5 >= self.initial_stack:
            return valid_actions[0]["action"], valid_actions[0]["amount"]
        # valid_actions format => [fold_action_info, call_action_info, raise_action_info]
        call_action_info = valid_actions[1]
        action, amount = call_action_info["action"], call_action_info["amount"]
        
        self.hole_card = [Card.from_str(card) for card in hole_card]
        # print(self.hole_card)
        
        self.com_card = [Card.from_str(card) for card in round_state['community_card']]
        # print(self.com_card)
        
        self.street = round_state['street']
        # print(self.street)
        
        self.rank = HandEvaluator.gen_hand_rank_info(self.hole_card, self.com_card)
        # print(self.rank)

        if(self.street == "preflop"):
            if(self.rank["hand"]["strength"] == "ONEPAIR"):
                if(self.rank["hole"]["high"] > 5):
                    if((self.rank["hole"]["high"] - 5) * 10 > valid_actions[2]["amount"]["min"] and valid_actions[2]["amount"]["min"] >= 0):
                        action = valid_actions[2]["action"]
                        amount = min(valid_actions[2]["amount"]["min"] + (self.rank["hole"]["high"] - 5) * 10, valid_actions[2]["amount"]["max"])
                    else:
                        call_action_info = valid_actions[1]
                        action, amount = call_action_info["action"], call_action_info["amount"]
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
            elif(self.rank["hole"]["low"] > 8):
                if((self.rank["hole"]["high"] + self.rank["hole"]["low"] - 18) * 10 > valid_actions[2]["amount"]["min"] and valid_actions[2]["amount"]["min"] >= 0):
                    action = valid_actions[2]["action"]
                    amount = min(valid_actions[2]["amount"]["min"] + (self.rank["hole"]["high"] + self.rank["hole"]["low"] - 18) * 10, valid_actions[2]["amount"]["max"])
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
            elif(self.rank["hole"]["high"] > 10):
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
            else:
                if(valid_actions[1]["amount"] > 20):
                    call_action_info = valid_actions[0]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
        elif(self.street == 'flop'):
            if(self.rank["hand"]["strength"] == ("STRAIGHTFLASH" or "FOURCARD")):
                if(valid_actions[2]["amount"]["min"] >= 0):
                    call_action_info = valid_actions[2]
                    action, amount = call_action_info["action"], call_action_info["amount"]["max"]
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
            elif(self.rank["hand"]["strength"] == ("STRAIGHT" or "FLASH" or "FULLHOUSE")):
                point = HandEvaluator.eval_hand(hole = self.hole_card, community = self.com_card)
                if(point // 12 > valid_actions[2]["amount"]["min"] and valid_actions[2]["amount"]["min"] >= 0):
                    action = valid_actions[2]["action"]
                    amount = min(point // 12, valid_actions[2]["amount"]["max"])
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
            elif(self.rank["hand"]["strength"] == ("THREECARD" or "TWOPAIR")):
                point = HandEvaluator.eval_hand(hole = self.hole_card, community = self.com_card)
                if(point // 20 > valid_actions[2]["amount"]["min"] and valid_actions[2]["amount"]["min"] >= 0):
                    action = valid_actions[2]["action"]
                    amount = min(point // 20, valid_actions[2]["amount"]["max"])
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
            elif(self.rank["hole"]["high"] == self.rank["hole"]["low"]):
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
            else:
                if(valid_actions[1]["amount"] > 3 * (self.rank["hole"]["high"] + self.rank["hole"]["low"])):
                    call_action_info = valid_actions[0]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
        elif(self.street == 'turn'):
            if(self.rank["hand"]["strength"] == ("STRAIGHTFLASH" or "FOURCARD")):
                if(valid_actions[2]["amount"]["min"] >= 0):
                    call_action_info = valid_actions[2]
                    action, amount = call_action_info["action"], call_action_info["amount"]["max"]
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
            elif(self.rank["hand"]["strength"] == ("STRAIGHT" or "FLASH" or "FULLHOUSE")):
                point = HandEvaluator.eval_hand(hole = self.hole_card, community = self.com_card)
                if(point // 20 > valid_actions[2]["amount"]["min"] and valid_actions[2]["amount"]["min"] >= 0):
                    action = valid_actions[2]["action"]
                    amount = min(point // 20, valid_actions[2]["amount"]["max"])
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
            elif(self.rank["hand"]["strength"] == ("THREECARD" or "TWOPAIR")):
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
            elif(self.rank["hole"]["high"] == self.rank["hole"]["low"]):
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
            else:
                if(valid_actions[1]["amount"] > 3 * (self.rank["hole"]["high"] + self.rank["hole"]["low"])):
                    call_action_info = valid_actions[0]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
        elif(self.street == 'river'):
            if(self.rank["hand"]["strength"] == ("STRAIGHTFLASH" or "FOURCARD")):
                if(valid_actions[2]["amount"]["min"] >= 0):
                    call_action_info = valid_actions[2]
                    action, amount = call_action_info["action"], call_action_info["amount"]["max"]
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
            elif(self.rank["hand"]["strength"] == ("STRAIGHT" or "FLASH" or "FULLHOUSE")):
                point = HandEvaluator.eval_hand(hole = self.hole_card, community = self.com_card)
                if(point // 40 > valid_actions[2]["amount"]["min"] and valid_actions[2]["amount"]["min"] >= 0):
                    action = valid_actions[2]["action"]
                    amount = min(point // 40, valid_actions[2]["amount"]["max"])
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
            elif(self.rank["hand"]["strength"] == ("THREECARD" or "TWOPAIR")):
                if(self.rank["hole"]["high"] == self.rank["hole"]["low"]):
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                elif(valid_actions[1]["amount"] > 4 * (self.rank["hole"]["high"] + self.rank["hole"]["low"])):
                    call_action_info = valid_actions[0]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
            elif(self.rank["hole"]["high"] == self.rank["hole"]["low"]):
                if(valid_actions[1]["amount"] > 4 * (self.rank["hole"]["high"] + self.rank["hole"]["low"])):
                    call_action_info = valid_actions[0]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                else:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
            else:
                point = HandEvaluator.eval_hand(hole = self.hole_card, community = self.com_card)
                if(point // 4 > valid_actions[1]["amount"]):
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                else:
                    call_action_info = valid_actions[0]
                    action, amount = call_action_info["action"], call_action_info["amount"]
        return action, amount  # action returned here is sent to the poker engine


    def find_name(self, seats, uuid):
        for s in seats:
            if s["uuid"] == uuid:
                return s["name"]

    def receive_game_start_message(self, game_info):
        self.max_round = game_info["rule"]["max_round"]
        self.initial_stack = game_info["rule"]["initial_stack"]
        self.small_blind = game_info["rule"]["small_blind_amount"]
        self.name = self.find_name(game_info["seats"], self.uuid)

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return AgentPlayer()
