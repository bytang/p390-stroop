# Software prerequisites

Python3  
`pygame` package

# Running an experiment

Run `stroop_group5.py` and follow the on-screen instructions.

# Experimental data

The script reads a predefined list of words, text colours, and delays. This allows us to maintain consistency between participants by showing each one the same stimuli.

## input data file

`data.csv` contains a predefined Stroop experiment that will be shown to each participant. Each row is one trial.

word: a word to show to participant

colour: a word from below corresponding to the text colour of the word

  - red rgb(230,38,0)
  - green rgb(38,230,0)
  - blue rgb(25,64,255)
  - yellow rgb(255,217,25)

condition: a string corresponding to the trial condition

  - congruent
  - incongruent

delay: milliseconds to wait before showing the trial word  
Can override to use a fixed delay.

block: a number 0-1 to indicate whether trial is training or experiment

  - 0: training trial to make sure participant understands task and controls
  - 1: experiment trial

## output data file

`session_YYYYMMDD_n.csv` contains measurements from one session of the Stroop experiment.

word, colour, cond, delay, RT, keypress, correct, block

word: the word shown to participant  
colour: the colour of the word  
cond: a number corresponding to the trial condition  
delay: milliseconds before showing the trial word  
RT: participant reaction time between showing trial word and pressing a button  
keypress: button participant pressed after trial word shown  
correct: whether the button matches the colour of the word  
block: what part of the experiment is the trial in  