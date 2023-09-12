# CLI-Flashcards
- Flashcards in a CLI game, use whatever data you want. Eg: Learn a language
- A mini hackathon project for myself as I try to learn Dutch

## Manual
### Data
- The data is stored in the data/somefile.csv
- The only requirement is that the first line of the file is the header (with two cols)
- You can have as many datafiles as you want, save them in the data folder
- eg: Dutch word, English word
- If you want multiple options, just separate them using "/". eg: okay,ok/alright
### Running the script
- To run the script, you need to have python installed. Then, you can run the script with the following command:
```bash
python3 main.py
```
- If you need are using other data files, you can specify the file with the following command:
```bash
python3 main.py --file "data/somefile.csv"
```
- Then you can follow the instructions on the screen.

## Features
- [x] Read data from a csv file
- [x] Multiple data files options
- [x] Verify columns
- [x] Randomize the order of the questions
- [x] Select the number of questions
- [x] Show the correct answer if the user fails
- [x] Ignore answers if user got it correct multiple times
- [x] Timer
- [x] Statistics
- [x] Save/Restore previous session
- [x] Show incorrect answers at the end for the session
- [x] Option to have multiple possible answers
