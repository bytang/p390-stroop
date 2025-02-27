# Software prerequisites

Python3  
`pygame` package

# Experimental data

## input data file

`data.csv` contains the predefined Stroop testing data that will be shown to each participant. Each row is one trial.

word: a word to show to participant

colour: a letter corresponding to the text colour of the word

  - r: red rgb(230,38,0)
  - g: green rgb(38,230,0)
  - b: blue rgb(25,64,255)
  - y: yellow rgb(255,217,25)

cond: a number 0-1 corresponding to the trial condition

  - 0: congruent word colour pair
  - 1: incongruent word colour pair

block: a number 0-1 corresponding to trial being training or experiment

  - 0: training trial to make sure participant understands task and controls
  - 1: experiment trial

## output data file

`session_YYYYMMDD_n.csv` contains measurements from one session of the Stroop experiment.