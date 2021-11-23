import matplotlib.pylab as plt
from IPython import display

class DQNPlotting:
    '''
    Class used to graphically present different aspects of DQN Learning.
    
    One of the things I would like to get a better look into is:
        - Which states were most visited
        - Which states were most used while training
        
    Class works by creating Axes. It periodically draws over the Axes or redraws the whole thing.
    '''
    
    def __init__(self):
        rows = 1
        columns = 2
        self.fig, self.ax = plt.subplots(rows, columns, figsize=(15, 10))
        
        
        
    def draw(self, graph_data, data_clear=False):
        '''
        PARAMS
            data     <dictionary>   Dictionary, where "key" is the axes we want to draw the data. Value is the data we want to plot
                                        Example:
                                            {(1,2): {
                                                "x": [1,2,3],
                                                "y": [4,5,6]
                                                }
                                                "draw_mode": "scatter"
                                                "x_label": "num_of_episodes",
                                                "y_label": "reward"
                                            }
            clear    <boolean>      If True, it will clear the Axes before drawing.
        
        RETURNS
        
        '''
        
        
        if data_clear:
            print("ADD FUNCTIONALITY WHEN WE WANT TO CLEAR AXES")
            pass # TO-DO add the clearing part of code
        
        for key, value in graph_data.items():
            if value["draw_mode"] == "scatter":
                self.ax[key].scatter(value["x"], value["y"], c=value["c"], alpha=0.005)
                self.ax
            elif value["draw_mode"] == "plot":
                self.ax[key].plot(value["x"], value["y"], c=value["c"])
            self.ax[key].set_xlabel(value["x_label"])
            self.ax[key].set_ylabel(value["y_label"])
        display.display(plt.gcf())
        display.clear_output(wait=True)
        
    