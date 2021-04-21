# Exam Number: Y3850518

from psychopy import event, gui, visual, core

from csv import DictWriter

from random import shuffle, uniform

import numpy as np

########################## STROOP TASK EXPERIMENT ############################

# Script presents a Stroop Task through Psychopy. See attached Lab Wiki for details.

########################### CHANGE EXPERIMENT PARAMTERES ######################

# For simpler data analysis following experiment, length of each identifcation numbers 
# can be specified.  Change ID_LEN to 3 if you have more than 99 participants. 
ID_LEN = 2

# Participants will be given practice trials to ensure they understand the 
# task.  Change NUMBER_OF_PRACTICES to specify number of practice trials. 
NUMBER_OF_PRACTICES = 6

# Participants will recieve a break after every n trials, depending on what 
# BREAK_INTERVAL is set to. Set to either 20, 30 or 60.
BREAK_INTERVAL = 30

# Set SHOW_RESULTS to True if you wish participants to see their performance 
# scores following the experiment.  Otherwise set it to False. 
SHOW_RESULTS = True

# Set CNUMBER to number of congruent trials you wish to appear in the
# experiment (default = 15). 
CNUMBER = 15

# Set INUMBER to number of incongruent trials you wish to appear in 
# the experiment (default = 5). 
INUMBER = 5

# Configure a jittered interstimulus interval using floating point numbers, 
# utilising 'uniform(a, b)'. Set argument 'a' to lowest number and 'b' to 
# highest
JITTER = uniform(.1, 1)

######################## GET PARTICIPANT ID ################################
           
# Declare dictionary to store details of the experiment which will be included
# in the pop-up box at the beginning of experiment. 
data1 = {}
data1['Experiment Name'] = 'The Stroop Task'
data1['Identification Number'] = ''

# A 'while loop' ensures that all of the following conditions are met.
while True:
    
    # Set up dialog box, fix 'Experiment Name', and set the order of fields.
    info = gui.DlgFromDict(data1, title='Input Details', fixed=['Experiment Name'],
                        order=['Experiment Name', 'Identification Number'])

    # If partcipant or investigator chooses to cancel, quit the experiment 
    # and print a message to the screen.
    if not info.OK:
        print("The experiment has been cancelled")
        core.quit()
        
    # Set up input variable, where participant's ID number must be entered.
    inpt = data1['Identification Number'] 

    # Ensure ID entered is specified number length. If input doesn't match requirements 
    # (number of certain length), present error message and opportunity to try again.
    if len(inpt) != ID_LEN or not inpt.isnumeric():
        error = gui.Dlg(title="Error")
        error.addText('Please enter a %d digit number.' % ID_LEN)
        error.show()
        
        if not error.OK:
            print("The experiment has been cancelled")
            core.quit()
        continue
    
        # Exit from loop if conditions above are satisfied.
    else:
        break
        
# Generate filename using the participant's ID number.
filename = 'P%s.csv' % (inpt)

########################## SET UP STIMULUS ################################

# Create window, and set up classes with parameters which will be used to 
# present trial stimuli and end, break, practice, and introductory stimuli. 
win = visual.Window([1024, 768], fullscr = False, \
                    allowGUI=True, units="pix", color = (-1, -1, -1))

trial_stim = visual.TextStim(win, text = "")

stim = visual.TextStim(win, text = "", color = (1, 1, 1))

# Set up practice run, introduction, break and end stimuli which will be shown to
# participant throughout the experiment. 
pr_intro = """Welcome!\n\nYour task is to determine the colour of the words \
presented to you.\n\nAs you can see, the keyboard has four coloured stickers \
(red, blue, yellow and green). You should use these to submit your answers, \
hitting the button that corrosponds to the COLOUR of the word presented, \
ignoring the actual word.\n\nTry to do this as quickly and as accurately as \
possible.\n\nYou will do this for 120 words. Don't worry! You'll get a break \
every %d words.\n\nLet's start with a practice run. Press SPACE to begin.
""" % (BREAK_INTERVAL)

wrong = "Incorrect! Be sure to choose the colour, not the word.\n\nPress \
SPACE to continue."

right = "Correct!\n\nPress SPACE to continue."

introduction = """Good job!\n\nIf you still feel unsure about the task, \
please ask the experimenter. If you're feeling confident, feel free to continue.\n
Be aware that you will not be informed as to whether you were correct after \
each trial like in the practice. You will also be given a 3 second countdown \
following this page and following the breaks, which will give you time to get \
your fingers in place.\n\nReminder: Try respond as quickly and as accurately \
as possible.\n\nIf you're ready, hit SPACE.
"""

breaks = """Good job! Feel free to take a short break, otherwise, continue \
the task by pressing SPACE.
"""

end = """You have now completed the stroop task!\n\nYour participation is \
greatly appreciated and will contribute to the science of processing speed \
and selective attention. Thank you!\n\nYou may now press SPACE to exit the \
experiment.
"""

############################### FUNCTIONS ###################################

# Set text, draw and present to window.  Requires keypress.
# This can be called within the script using relevant stimulus.
def present_stim(stimulus):
    stim.setText(stimulus)
    stim.draw()
    win.flip()
    event.waitKeys(keyList = ['space'])
    
# Countdown from 3 to 1, and present to screen. Calling this allows participants 
# time to place fingers on keys.
def count():
    for num in range(3, 0, -1):
        stim.setText(num)
        stim.draw()
        win.flip()
        core.wait(1)

# Calculates means for each condition, as well as percentage correct.
# This calculates how well each subject performs, which can be presented at the 
# end of experiment if investigator wishes.
def means_percentages(dictionary1):
    percentage = dictionary1['right'].count(True)*100.0 / len(dictionary1['right'])
    c_mean = float(np.mean(dictionary1['congruent']))
    i_mean = float(np.mean(dictionary1['incongruent']))
    
    return percentage, c_mean, i_mean

# Save colour text with associated keypress letter in dictionary.
# This will be used later to deterimine accuracy and response of each participant. 
rkeys = {'red': 'r', 'blue': 'b', 'green': 'g', 'yellow': 'y'}

# Set up dictionary to store reaction times for each condition, and response data.
# This will allow stroop performance to be presented at the end of experiment. 
results_dict = {'congruent' : [], 'incongruent' : [], 'right' : []}

########################## SET UP TRIALS ##########################################

# Set up list to store all 120 trials. 
all_trials = []

# Set up words and colours list for individual trial creation.
words_colours = ['red', 'green', 'blue', 'yellow']

# Loop through list once and then again within that loop.
for word in words_colours:
    for colour in words_colours:
        # Set number of congruent and incongruent trials. 
        num = CNUMBER if word == colour else INUMBER
        # Extend pairs of words to list and multiply by specified number.
        all_trials.extend([[word, colour]]*num) 

# Randomise trial order.
shuffle(all_trials)

######################### BEGIN PRACTICE EXPERIMENT ##########################

# Draw and show practice introduction stimulus. 
present_stim(pr_intro)

# Iterate through trials, and keep track of the index. 
for iteration, pr_trial in enumerate(all_trials):
    
    # Break from loop once practice limit has been reached using index. 
    if iteration == NUMBER_OF_PRACTICES:
        break
        
    # Save current text and colour. 
    pr_text = pr_trial[0]
    pr_colour = pr_trial[1]
    
    # Set colour and text of current trial and display.
    trial_stim.setText(pr_text)
    trial_stim.setColor(pr_colour)
    trial_stim.draw()
    win.flip()
    
    # Require keypress from 4 colour associated letters.
    pr_res = event.waitKeys(keyList = ['r', 'b', 'g', 'y'])
    
    # Calculate accuracy (True vs False) by comparing actual keypress with 
    # correct keypress using rkeys dictionary defined earlier. 
    pr_correct = (pr_res[0] == rkeys[pr_colour])
    
    # Present different stimulus following keypress, depending on subject's accuracy.
    # This reminds participant of the task if they give an incorrect answer.
    present_stim(right) if pr_correct == True else present_stim(wrong)

######################### BEGIN REAL EXPERIMENT ##############################

# Present introductory stimulus and countdown from 3.
present_stim(introduction)
count()

# Open previously created file, and use DictWriter to set relevant headings.
f = open(filename, 'w')
write = DictWriter(f, fieldnames=['trialnum', 'colourtext', 'colourname', \
                                   'condition', 'response', 'rt', 'correct'])
write.writeheader()

# Iterate though all trials, keeping track of the index.  Specify that
# the index starts at 1 - which wil be used to print trial number. 
for trialnum, trial in enumerate(all_trials, 1):  
    
    # Allow break every n trials to ensure participant doesn't get fatigued.
    # This can be specified at the top of script. 
    if (trialnum - 1) > 0 and (trialnum - 1) % BREAK_INTERVAL == 0:
        present_stim(breaks)
        count()
    
    # Present jittered inter-stimulus interval between trials.
    win.flip()
    core.wait(JITTER)
       
    # Save current text and actual colour of text into the appropriate variables.
    colourtext = trial[0]
    colourname = trial[1] 
   
    # Set text and colour for individual trial, and draw this to window.
    trial_stim.setText(colourtext)
    trial_stim.setColor(colourname)
    trial_stim.draw()

    # Present the trial stimulus, and at the same time set time of onset which 
    # will be used to deterime time since stimulus onset to time of keypress (reaction time).
    displaytime = win.flip()

    # Time stamp and wait for keypress. Set time since onset to calcualte 
    # participant's reaction time (time of keypress - onset of stimulus), and store
    # key subject pressed. 
    res = event.waitKeys(keyList = ['r', 'b', 'g', 'y'], timeStamped = True)
    rt = res[0][1] - displaytime
    key_response = res[0][0]
    
    # Using rkeys dictionary, determine whether participant's response was accurate
    # or not. 
    correct = (key_response == rkeys[colourname])

    # Switch keys and values of rkeys dictionary, and store colour associated 
    # with participant's keypress to gather participant's actual colour response.
    value_dict = dict((letter, colour) for colour, letter in rkeys.items())
    response = value_dict[key_response]

    # Determine if condition is congruent or incongruent by comparing colourtext 
    # with colourname. 
    condition = 'congruent' if colourtext == colourname else 'incongruent'
    
    # Attach data to correct column in the file that was previously set up.
    header_rows = {'trialnum': trialnum, 'colourtext': colourtext, \
                   'colourname': colourname, 'condition': condition, \
                   'response': response, 'rt': rt, 'correct': correct}

    write.writerow(header_rows)
    
    # Append accuracy values and reaction times to dictionary so percentage of 
    # correct responses can be calculated - which can then be presented to participant.
    results_dict['right'].append(correct)
    results_dict[condition].append(rt)

f.close()

############################# END EXPERIMENT ###############################

# Present results to participant.  If you do not wish participants to 
# see their results, set 'SHOW_RESULTS' to False at top of script.
if SHOW_RESULTS:

    # Calculate percentage correct and reaction time means for conditions. 
    percentage, c_mean, i_mean = means_percentages(results_dict)

    # Set up results stimulus with appropriate values to present if experimenter wishes.
    results = ("Well done! You got...\n\n\n%.2f%% Correct!\n\nCongruent Mean Reaction Time: \
%.3f seconds\n\nIncongruent Mean Reaction Time: %.3f seconds.\n\n\nPlease press SPACE to continue.") \
    % (percentage, c_mean, i_mean)
    
    present_stim(results)

# Present ending stimulus, close window and quit. 
present_stim(end)
win.close()
core.quit()
