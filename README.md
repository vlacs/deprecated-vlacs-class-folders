# vlacs-class-folders #

The purpose of this project is to automate the task of creating a folder structure on Google Drive and synchronizing
between teachers and students of each class appropriately.

## Implementation ##

The following will be implemented using Python.

* Create and share folders between teachers and students.
* Automatically add new students, teachers, and classes.
* Automatically archive student / class folders upon completion or drop.
* Initial batch to insert current students, teachers, and classes.

## Structure ##
* Classes
  + [Client.py](https://github.com/vlacs/vlacs-class-folders/blob/master/Classes/Client.py)     (Easily create Google Data Client)
  + [Database.py](https://github.com/vlacs/vlacs-class-folders/blob/master/Classes/Database.py)   (Connect to Database and run queries)
  + [Folder.py](https://github.com/vlacs/vlacs-class-folders/blob/master/Classes/Folder.py)     (Create, Share, and Unshare Folders on Google Drive)
* Files
  + [create_structure.py](https://github.com/vlacs/vlacs-class-folders/blob/master/create_structure.py) (Run once to create Database Tables and root folders)
  + [daily_cron.py](https://github.com/vlacs/vlacs-class-folders/blob/master/daily_cron.py) (Run daily with cron to check for dropped / created classes and archive folders)
  + [run_batch.py](https://github.com/vlacs/vlacs-class-folders/blob/master/run_batch.py)  (Pull data from Postgres and Create / Share Folders for students and teachers)
  + [utilities.py](https://github.com/vlacs/vlacs-class-folders/blob/master/utilities.py)  (Optional manual tasks. Unshare, Unarchive, etc.)

## Dependencies ##
* python
* python-dev
* gdata
* pyscopg2
* libpq-dev

## Instructions ##
Before you run the first batch be sure to run create_structure.py so you have the root folders in
Google Drive and the tables in the Postgres Database.

Also, be sure that the database has the proper view in it ([view.sql](https://github.com/vlacs/vlacs-class-folders/blob/master/view.sql))

Now you are ready to run a batch, here is the command line syntax:
:$ python run_batch.py <limit> <offset>

For the first batch it will be fine just to provide a limit, or if you'd like to process the entire
database you will not need to provide any parameters.

After the first batch you can use the offset parameter to process the next set of records.

Currently the script orders by the master id and classroom id.

This program is intended to run on an internal VLACS server (Ubuntu) but it should run anywhere
Python, GData, and psycopg2 will.

### License ###
vlacs-class-folders by [Mike George](http://mikegeorge.org) is licensed under a [Creative Commons Attribution-ShareAlike 3.0 United States License](http://creativecommons.org/licenses/by-sa/3.0/us/deed.en_US).

<p align="center"><a href="http://vlacs.org/" target="_blank"><img src="http://vlacs.org/images/VLACS_logo_no_dep_website.png" alt="VLACS Logo"/></a><br /><a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/us/deed.en_US"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/us/88x31.png" /></a></p>
