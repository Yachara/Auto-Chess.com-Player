import gym
from gym import wrappers
from time import time
import matplotlib.pyplot as plt

if __name__ == "__main__":
    scores = []
    EPISODES = 1000
    render_every_ep = 1
    video_record_every_ep = 1
    good_episodes = None
    
    env = gym.make("LunarLander-v2")
    env = gym.wrappers.Monitor(env, "./videos/"+str(int(time()))+"/", video_callable=lambda episode_id: episode_id%video_record_every_ep==0)
    env._max_episode_steps = 4000 # changes the max steps in an episode
    
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    agent = DQNAgent(state_size, action_size, good_memory=good_episodes)
    agent.gamma=0.99         # reward discount rate
    agent.epsilon=0.3        # exploration rate
    agent.epsilon_min=0.01
    agent.epsilon_decay=0.99
    agent.batch_size=32
    agent.train_start=600   # when we have this many individual memories, the training can start
    agent.memory.max_good_episodes = 3
    agent.memory.max_bad_episodes = 3
    
    graph = None#DQNPlotting()
    
    #agent.load("./models/DQN_T1604241703_R57.1_E200.h5")
    scores = run(env=env, 
                 agent=agent, 
                 EPISODES=EPISODES, 
                 render_every_ep=render_every_ep,
                 graph=graph,
                )
    '''
    
    scores = test(env=env,
                  agent=agent,
                  EPISODES=EPISODES,
                  render_every_ep=render_every_ep,
                  graph=graph
                  )
    '''



fig, ax1 = plt.subplots(1,1,figsize=(8,8))
ax1.plot(scores)
ax1.plot([np.mean(scores[i-100:i]) for i in range(len(scores))])
plt.show()