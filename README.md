# vlacs-class-folders #

The purpose of this project is to automate the task of creating a folder structure on Google Drive and synchronizing
between teachers and students of each class appropriately.

## Implementation ##

A command that can be run on a timed schedule (cron) to keep Google Drive synced between
students and teachers based on enrollments. The system automatically archives folders 
after a student completes the class, drops the class, or fails the class.

The system also handles name changes for both students and teachers.

## Structure ##
* Config
  + [config.sample.py](https://github.com/vlacs/vlacs-class-folders/blob/master/Config/config.samply.py) - (Must be renamed to config.py)
* Libraries
  + [Client.py](https://github.com/vlacs/vlacs-class-folders/blob/master/Libs/Client.py) -------- (Easily create Google Data Client)
  + [Color.py](https://github.com/vlacs/vlacs-class-folders/blob/master/Libs/Color.py) -------- (Utility lib used to output colored text to console)
  + [Database.py](https://github.com/vlacs/vlacs-class-folders/blob/master/Libs/Database.py) --- (Connect to Database and run queries)
  + [Folder.py](https://github.com/vlacs/vlacs-class-folders/blob/master/Libs/Folder.py) ------- (Create, Share, and Unshare Folders on Google Drive)
  + [Share.py](https://github.com/vlacs/vlacs-class-folders/blob/master/Libs/Share.py)  ------- (Library that contains sharing functions and logic)
  + [Sync.py](https://github.com/vlacs/vlacs-class-folders/blob/master/Libs/Sync.py) -------- (Contains all the boolean functions used when syncing Google Drive with Database)
  + [Utilities.py](https://github.com/vlacs/vlacs-class-folders/blob/master/Libs/Utilities.py) ------ (Useful methods that can be used throughout the codebase)
* Objects
  + Contains various python objects that are used throughout the code.
* Files
  + [run.py](https://github.com/vlacs/vlacs-class-folders/blob/master/run.py) ----------- (All-in-One file, check structure of db and google drive, sync, update, etc.)

## Dependencies ##
* python
* python-dev
* gdata
* pyscopg2
* libpq-dev

## Instructions ##
First, be sure that your database has the proper view in it ([view.sql](https://github.com/vlacs/vlacs-class-folders/blob/master/view.sql))

Now you are ready to run a batch, here is the command line syntax:
```
python run.py [--limit <limit> --offset <offset>]
```
or
```
python run.py [-l <limit> -o <offset>]
```
The first time you run the program it will be fine just to provide a limit, or if you'd like to process the entire
database you will not need to provide any parameters.

After the first batch you can use the offset parameter to process the next set of records.

Currently the script orders by the master id and classroom id.

This program is intended to run on an internal VLACS server (Ubuntu) but it should run anywhere
Python, GData, and psycopg2 will.

### License ###
vlacs-class-folders by [Mike George](http://mikegeorge.org) is licensed under a [Creative Commons Attribution-ShareAlike 3.0 United States License](http://creativecommons.org/licenses/by-sa/3.0/us/deed.en_US).

<p align="center"><a href="http://vlacs.org/" target="_blank"><img src="http://vlacs.org/images/VLACS_logo_no_dep_website.png" alt="VLACS Logo"/></a><br /><a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/us/deed.en_US"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/us/88x31.png" /></a></p>
