# League Skills Priority
A simple study of champions' skill-leveling priority in League of Legends

The goal of this simple project is to see if there is a pattern in Riot's champion design when it comes to
what skills are essential to a champion.

In data_collector.py the information about champions (names and classes) is pulled from Riot's static data. It automatically pulls the information for the lastest patch. Then, the information about the skill leveling priority for each of them is scrapped from champion.gg
The aformentioned information information is saved in a csv file ('champions.csv') and different features are plotted with data_plotter.py


