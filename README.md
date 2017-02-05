# Represenation of Android package memory usease in graphical way 

prerequisites:
  python
  matlpotlib
  numpy
 
 Usage:
  This graph will be useful in debugging memory leaks/memory used by a package in long run Tests e.g Stability. 
 
Procedure:
Generate meminfo file by using install.bat present inside meminfo folder for 7200 minutes(time can be changed by editing for loop in meminfo.bat)

Put the Android Package name, corresponding color scheme, type of graph, max memory of DUT meminfo filename inside plotgraph.xml
  run plotgraph.py using "python plotgraph.py"
  
