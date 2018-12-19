# League_Skills_Priority
A simple study of champions' skill-leveling priority in League of Legends

The goal of this simple project is to see if there is a pattern in Riot's champion design when it comes to
what skills are essential to a champion

In data_collector.py, given the list of champions of League of Legends, the information about the skill 
leveling priority for each of them is scrapped from champion.gg
This information is saved in a csv file ('champions.csv') and different features are plotted with data_plotter.py

Thanks to gitHub user ngryman for the champions.json file used to build the list containing all champions' names. 
Link to his repository: github.com/ngryman/lol-champions
