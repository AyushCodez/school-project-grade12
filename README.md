# school-project-grade-12

Grade 12 school project


-----

System monitoring tool	tkinter -> for ux, matplotlib -> for graphs, csv -> for reading csv files, pillow -> image handling, (psutil, os, sys, MacTmp) -> for data gathering + more based on requirements as they arise.	
CSV, SQL

-----

## PLAN

- TKINTER GUI
- CPU UTILIZATION, MEMORY UTILIZATION, DISK UTILIZATION.
- GRAPHING WITH MATPLOTLIB, SHOWING IT WITH PILLOW. PILLOW TO EXPORT GRAPHS TO PNG.
- CSV FOR EXPORTING DATA TO CSV.
- SQL FOR PREVIOUS DATA STORAGE.
- PSUITL, OS, SYS, MACTMP FOR DATA GATHERING. EVERY 100 MS, ADD EVERY SECOND.
- SHOW GRAPH FROM CSV.
- WE WILL HAVE HISTORICAL DATA FOR 4 HOURS.
- historical if laptop off, then show previous historical when laptop on - duration pickers will have date/time accordingly...

-----

## GUI

- like intel power gadget
- 3 tabs - "Current", "Historical", "Read CSV"
- Current tab:
    - current values, like IPG. Show graphs, update every 1 sceond, data poll every 1 second.
    - CPU Utilization
    - Memory Utilization
    - CPU Temperature
    - Disk Utilization
- Historical tab:
    - DURATION picker
    - only show graphs
    - CPU Utilization
    - Memory Utilization
    - CPU Temperature
    - Disk Utilization
- Read CSV tab:
    - Read CSV file
    - Show graph from CSV file
    
-----

