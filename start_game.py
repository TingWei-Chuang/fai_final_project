import json
from game.game import setup_config, start_poker
from agents.call_player import setup_ai as call_ai
from agents.random_player import setup_ai as random_ai
from agents.console_player import setup_ai as console_ai
from agents.if_else_player import setup_ai as if_else_ai
from agents.sample_brave_player import setup_ai as sample_brave_ai
from agents.sample_player import setup_ai as sample_ai
import numpy as np

from matplotlib import pyplot as plt

from baseline0 import setup_ai as baseline0_ai
from baseline1 import setup_ai as baseline1_ai
from baseline2 import setup_ai as baseline2_ai
from baseline3 import setup_ai as baseline3_ai
from baseline4 import setup_ai as baseline4_ai
from baseline5 import setup_ai as baseline5_ai
from baseline6 import setup_ai as baseline6_ai
from baseline7 import setup_ai as baseline7_ai

test = {
    "b4": baseline4_ai,
    "b5": baseline5_ai,
    "b6": baseline6_ai,
    "b7": baseline7_ai,
}

agent_name = "sample_brave"
save_fig_path = "performance/sample_brave.png"

barWidth = 0.5
 
bar_x = np.arange(len(test))
N = 15

for i_alg, (name, alg) in enumerate(test.items()):
    print(f"competitor {name}")
    n_wins = 0
    for i in range(N):
        print(f"test {i}")
        config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
        config.register_player(name=agent_name, algorithm=sample_brave_ai())
        config.register_player(name=name, algorithm=alg())
        game_result = start_poker(config, verbose=4)
        for player in game_result["players"]:
            if player["name"] == agent_name:
                if player["stack"] > 1000:
                    print("win")
                    n_wins += 1
                else:
                    print("lose")
                break
    win_rate = n_wins / N
    print(f"my agent win rate: {win_rate}")
    plt.bar(bar_x[i_alg], win_rate, width=barWidth, color='b')
plt.xlabel("Competitor")
plt.xticks(bar_x, list(test.keys()))
plt.ylabel("My Agent Win Rate")
plt.ylim(0., 1.)

plt.savefig(save_fig_path)





## Play in interactive mode if uncomment
#config.register_player(name="me", algorithm=console_ai())
#game_result = start_poker(config, verbose=1)

#print(json.dumps(game_result, indent=4))
