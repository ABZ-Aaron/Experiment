
from csv import DictReader

from os.path import basename

from re import sub

from glob import glob

from pylab import boxplot, xlabel, ylabel, xticks, title, savefig

import pylab as plt

import numpy as np

########################## ANALYSING DATA ###########################

# This script analyses data for all subjects, calcualting reaction time
# means and standard deviations, as well as percentage correct - for both 
# congruent and incongruent conditions.  The same values are calculated for 
# the group and all values are printed to a table. Script also produces a 
# boxplot showing mean reaction times for group for both conditions. 

########################## SET UP FUNCTIONS ################################
       
# Calculate means and standard deviations (std) for each participant for 
# conditions.
def means_stds(dictionary):
  
    for k, v in dictionary.items():       
        if k == 'congruent':   
            mean1 = np.mean(v); std1 = np.std(v)                          
        else:
            mean2 = np.mean(v); std2 = np.std(v)    
            
    return mean1, std1, mean2, std2
    
# Calculate the percentages of correct trials for each participant for both 
# conditions.
def percentages(dictionary1):
        
    for k, v in dictionary1.items():      
        if k == 'congruent':
            # Set 100.0 to ensure a float is returned.
            per1 = v.count('True')*100.0 / len(v)
        else:
            per2 = v.count('True')*100.0 / len(v)     
            
    return per1, per2

# Calcualte group means, stds, and percentages from the array created.  Done 
# through specifying columns and analysing all data in each one. 
def group_scores(group):   
    
    # Calculate means for both conditions.
    mean1 = group.mean(axis=0)[0]; mean2 = group.mean(axis=0)[1]
    
    # Calculate standard deviations for both conditions. 
    std1 = group.std(axis=0)[0]; std2 = group.std(axis=0)[1]
    
    # Calculate percentage correct for both conditions.
    perc1 = group.mean(axis=0)[2]; perc2 = group.mean(axis=0)[3]    
    
    return mean1, mean2, std1, std2, perc1, perc2

############################ SET UP TABLE ####################################

# Set up table to display final values, set up formatting for when data needs 
#to be printed to the table, and set up table lines by calculating length ot 
# titles. 
titles = "| Participant   |  Congruent (s)             | Incongruent (s)          |"
subtitles = "|               |  Mean  | Stddev | % Corr   | Mean  | Stddev | % Corr  |" 
structure = '| {:^12}  | {:0.3f}  | {:0.3f}  |  {:6.2f}  | {:0.3f} | {:0.3f}  | {:6.2f}  |' 
h_lines = '=' * len(titles)

# Print out table headings along with horizontal lines.
print(h_lines)
print(titles)
print (subtitles)
print(h_lines)

################## LOOP THROUGH FILES, STORE, AND PRINT DATA ################

# Save filenames in directory which end in .csv, and sort them in order. 
filenames = sorted(glob('/Users/aaronwright/Documents/Work & Uni/University/Neuroscience - UoY/Python/Assessement Two/data/*.csv'))

# Create an 'empty' array (all zeros) with 4 columns, and rows equal to number of 
# files in directory.  This will be used calculate group means, stds, and percentages.
filetotal = len(filenames)
group = np.zeros((filetotal, 4), float)

# Open, and read files using DictReader to obtain the data. Keep track of index, 
# which will be used to store data in array for group analyses. 
for index, filename in enumerate(filenames): 
    f = open(filename)
    reader = DictReader(f)
    
    # Subsitute .csv in file basename with empty string. This prints actual participant
    # ID, incase there are files missing from directory.
    participant = sub('\.csv', '', basename(filename))
        
    # Create dictionaries to store reaction times and correct values for each condition.
    rts = {}
    correct = {}
    
    # Loop through lines in the file to access data and close on exit.
    for line in reader:  
        
        # Define the columns needed for the analysis.
        condition = line['condition']
        reaction = float(line['rt'])
        accuracy = line['correct']
                 
        # Add conditions as keys to a dictionary, and append associated reaction 
        # times as values. Do the same for accuracy (correct) values. 
        rts.setdefault(condition, []).append(reaction)
        correct.setdefault(condition, []).append(accuracy)                                               
    
    f.close()
           
    # Calculate mean, std and 'correct' percentages for each participant for each condition, 
    # using the dictionaries that now store each condition and their assoicated values. 
    meanc, stdc, meani, stdi = means_stds(rts)    
    perc, peri = percentages(correct)
    
    # Store means and percentages for each condition into the array created earlier. 
    # Use the enumerate function to specify what row should be appended to on each iteration.  
    group[index] = [meanc, meani, perc, peri]
            
    # Print means, stds, and percentages for each participant, using the format 
    # created earlier. 
    print(structure.format(participant, meanc, stdc, perc, meani, stdi, peri))       
    print(h_lines)

############ PERFORM CALCULATIONS FOR GROUP AND PRINT TO TABLE #############

# Calculate the group means, stds and percentages, using the array containing 
# individual means and percentages, and print to table.
meancg, meanig, stdcg, stdig, percg, perig = group_scores(group)

print(structure.format('* Group *', meancg, stdcg, percg, meanig, stdig, perig))        
print(h_lines)

######################## PLOT DATA (BOXPLOT) ##############################

# Delete the last two columns of the array, keeping the 'mean' columns which
# can then be used to to plot the figure. 
group = np.delete(group, [2,3], axis=1)

# Set the style for the plot for a more professional look. 
plt.style.use('ggplot')

# Set up boxplot using group means, and set patch artist to True to allow
# for customisation. 
bp = boxplot(group, patch_artist=True)

# Label the conditions which will appear along the x axis of the plot. 
# Label the x and y axis, and create a plot title, setting fontweights to bold.
xticks([1, 2], ['Congruent', 'Incongruent'])
xlabel('Condition', fontweight='bold')
ylabel('Reaction Time (ms)', fontweight='bold')
title('Mean group reaction times for congruent and incongruent trials', y = 1.05, fontweight='bold')

# Edit the plot created, by changing colours and linewidths of whiskers, caps, etc.
for b in bp['boxes']:
    b.set(facecolor='silver', linewidth=1.5)
for w in bp['whiskers']:
    w.set(color='blue', linewidth=2)
for c in bp['caps']:
    c.set(color='blue', linewidth=2)
for m in bp['medians']:
    m.set(color='blue', linewidth=1.5)
for f in bp['fliers']:
    f.set(marker = 'o')

# Save the boxplot. 
savefig('group.png')
