<p align="right"><a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/us/deed.en_US"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/us/88x31.png" /></a></p>
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
  + [daily_cron.py](https://github.com/vlacs/vlacs-class-folders/blob/master/daily_cron.py) (Run daily with cron to check for dropped / created classes and archive folders)
  + [run_batch.py](https://github.com/vlacs/vlacs-class-folders/blob/master/run_batch.py)  (Pull data from Postgres and Create / Share Folders for students and teachers)
  + [utilities.py](https://github.com/vlacs/vlacs-class-folders/blob/master/utilities.py)  (Optional manual tasks. Unshare, Unarchive, etc.)

This program is intended to run on an internal VLACS server (linux) and will leverage the GData Python Client Library.
When it's finished it should be able to run anywhere python does.

<p align="center"><a href="http://vlacs.org/" target="_blank"><img src="http://vlacs.org/images/VLACS_logo_no_dep_website.png" alt="VLACS Logo"/></a></p>
