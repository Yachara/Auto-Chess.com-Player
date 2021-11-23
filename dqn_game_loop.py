def run(env,
        agent,
        EPISODES,
        render_every_ep,
        graph,
       ):
    
    scores = [0,]
    try:
        for episode in range(EPISODES):
            state = env.reset()
            agent.memory.reset_episode_memory()
            done = False
            total_reward = 0
            steps = 0
            
            while not done:
                if episode%render_every_ep==0:
                    env.render()              
                    
                action = agent.get_action(state)
                if graph != None:
                    '''
                    graph_data = {
                        (0,): {
                            "x": state[0][0],
                            "y": state[0][1],
                            "draw_mode": "scatter",
                            "x_label": "position",
                            "y_label": "velocity",
                        },
                    }
                    graph.draw(graph_data)
                    '''
                    pass

                next_state, reward, done, _ = env.step(action)
                steps += 1
                
                if steps >= env._max_episode_steps:
                    '''
                    Need to manualy implement since Wrappers does not end when it reached _max_episode_steps
                    '''
                    #print("MAX STEPS")
                    env.stats_recorder.save_complete()
                    env.stats_recorder.done = True
                    reward = -100
                    pass
                    
                total_reward += reward
                
                agent.remember(state, action, reward, next_state, done)
                state = next_state
                
                agent.train(graph)
                
                
            agent.update_exploring() # it makes more sense to change exploring after 1 whole episode is passed
            agent.memory.add_good_episode_to_memory(total_reward)
            agent.memory.add_bad_episode_to_memory(total_reward)
            # add episode to good and bad every time. If it has medium reward it goes to noone, else it goes to either bad or good
            scores.append(total_reward)
            
            
            we_won_str = "!! WINNER, WE WON !!" if reward == 100 else ""
            print(f"Ep: {episode}/{EPISODES}, Total_RWD: {total_reward:.1f}, Steps: {steps}/{env._max_episode_steps} e: {agent.epsilon:.2f}, Last_rwd: {reward}, {we_won_str}")                 
            
            
            if episode%50==0:
                model_name = f"DQN_T{int(time())}_E{episode}.h5"  # Naming convention is: DQN_<time>_<additional information>
                agent.save(path="./models/", model_name=model_name)
                with open("good_memory.pickle", "wb") as f:
                    pickle.dump(good_episodes, f)
                pass
            
            if graph != None:
                episode_moments = [moment[0] for moment in agent.memory.episode_memory]
                graph_data = {
                    (0,): {
                        "x": [state[0][0] for state in episode_moments],
                        "y": [state[0][1] for state in episode_moments],
                        "draw_mode": "scatter",
                        "x_label": "position",
                        "y_label": "velocity",
                    },
                    (1,): {
                        "x": [episode-1, episode],
                        "y": scores[-2:],
                        "draw_mode": "plot",
                        "x_label": "episode num",
                        "y_label": "episode reward"
                    }
                }
                graph.draw(graph_data)
            
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except Exception as e:
        print("ERROR")
        print(e)
    finally:
        env.close()
        return scores                