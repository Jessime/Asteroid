# -*- coding: utf-8 -*-
"""
Description
-----------

This is the most basic framework of the asteroid game.
It establishes a Model-View-Controller (MVC) pattern for coding design.
This should make it easier to work on different pieces at once. 

Here, the done flag and the time are passed from the model to the view.
The controller keeps track of time and check for user input. 

The 'game' starts when the screen is clicked,
and keeps track of the time indefiniately until the 'a' button is pressed.
Another click will then close the screen.

This is just a simple demonstrantion of how we're implementing MVC. 
"""

import time
import graphics as grf

class View():
    """Responsible for rendering the game, given the proper information

    Parameters
    ----------
    width : int
        The width of the GUI window
    height : int
        The height of the GUI window
        
    Attributes
    ----------
    win : grf.GraphWin
        The GUI window in which the game will be played
    time_time : grf.Text
        Shows the current time played in seconds
    done_text : grf.Text
        Shows whether or not the game is finished
    observed : dict
        All the variables received from the model
    """
    def __init__(self, width, height):
        self.win = grf.GraphWin('Asteroid', width, height)
        self.time_text = grf.Text(grf.Point(1100, 50), 'Time: 0')
        self.done_text = grf.Text(grf.Point(1100, 150), 'Done: False')
        self.observed = None
        
    def initialize(self):
        """Draw everything to the screen for the first time"""
        self.win.setBackground('white')
        self.time_text.draw(self.win)
        self.done_text.draw(self.win)
        
    def draw_done(self):
        """Update the 'Done' label"""
        self.done_text.setText('Done: {}'.format(self.observed['done']))
        
    def draw_time(self):
        """Update the 'Time' label"""
        self.time_text.setText('Time: {}'.format(int(self.observed['time'])))
        
    def update(self, observables):
        """Set the observed variables and update everything to the screen"""
        self.observed = observables
        self.draw_time()
        self.draw_done()
        
class Model():
    """Contains all of the core game logic
    
    Attributes
    ----------
    width : int
        The width of the gameplay space
    height : int
        The height of the gameplay space
    time : float
        The current length of time the game has been played
    done : bool
        Whether or not the game is finished yet
    observables : dict {str : attribute}
        Keeps track of all the attributes needed for the view
    """
    def __init__(self):
        self.width = 1200
        self.height = 800
        self.time = 0        
        self.done = False        
        self.observables = {'time': self.time,
                            'done': self.done}

    def set_time(self, time):
        self.time = time

    def update_observables(self):
        """Recreate observables dict to reflect current state of model"""
        self.observables = {'time': self.time,
                            'done': self.done}
                            
    def update(self, click, key):
        """Ends game of 'a' is pressed and updates the observables
        
        Returns
        -------
        done : bool
            Whether or not the game is finished yet
        """
        if key == 'a':
            self.done = True
        self.update_observables()
        return self.done
        
class Controller():
    """Handles time, user input, and passing data from model to view.
    
    Attributes
    ----------
    model : Model
        An instance of the Model class to run the game
    view : View
        An instance of the View class to render the game
    done : bool
        Flag to end the main loop
    click : grf.Point
        The location of the last click by the user
    key : str
        The name of the last key pressed by the user
    framerate : float
        The number of seconds per frame (technically inverse-framerate)
    start_time : float
        Initial start time of game. Used for referencing current length of game.
    """
    def __init__(self):
        self.model = Model()
        self.view = View(self.model.width, self.model.height)
        self.done = False
        self.click = None
        self.key = None
        self.framerate = 1/20        
        self.start_time = 0

    def check_user_input(self):
        """Record if the user has clicked the mouse or pressed a key"""
        self.click = self.view.win.checkMouse()
        self.key = self.view.win.checkKey()

    def update_time(self, loop_start):
        """Checks runtime of loop, sleeps if necessary, and sets model time

        Parameters
        ----------
        loop_start : float
            A time.time() measurement from the beginning of the loop
        """
        loop_end = time.time()
        execute_time = loop_end - loop_start
        if execute_time < self.framerate:
            time.sleep(self.framerate - execute_time)
        self.model.set_time(time.time() - self.start_time)
        
    def update(self):
        """Updates all portions of the gam (input, model, view, time).
        
        Returns
        -------
        done : bool
           Whether or not the game is finished yet         
        """
        loop_start = time.time()
        self.check_user_input()
        done = self.model.update(self.click, self.key)
        self.view.update(self.model.observables)
        self.update_time(loop_start)
        return done
        
    def run(self):
        """Main game loop"""
        self.view.initialize()
        self.view.win.getMouse()
        self.start_time = time.time()
        while not self.done:
            self.done = self.update()
        self.view.win.getMouse()
        self.view.win.close()
        
if __name__ == '__main__':
    controller = Controller()
    controller.run()