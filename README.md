To set up your automatic courses notification script, follow these steps.
(All files mentioned can be found in the exracted folder.)

1) Open the script.sh and replace the "path-to-script" with wherever you keep the new_cour.py script.

2) Don't change the export_x_info.sh script!!! :P

3) In your .bashrc add the line (this is same as the no_proxy in firefox)
	-> export no_proxy="localhost, 127.0.0.1, iiit.ac.in, .iiit.ac.in,iiit.net, .iiit.net, 172.16.0.0/12, 192.168.0.0/16, 10.0.0.0/8"
	
4) Change the permissions of new_cour.py, script.sh and export_x_info.sh to 755.

5) Check if you have all the imported libraries in new_cour.py installed (esp. keyring library). If not install them using apt-get, pacman etc.. sudo apt-get install python-<LibraryName>
**For Arch Linux, kering is not available, so you need to harcode the username
and password**

6) Run new_cour.py (Follow Instructions carefully !! After execution check the newly created folders.)

7) Schedule your scrpit. ( See Below )

8) Restart Your Computer.



Now there are two ways to schedule this script.
Way 1 ---- Crontab (Preferred and Tested)

1) Open Startup Applications and add export_x_info.sh in it. (DIY :P) This will run export_x_info.sh everytime comupter starts.

2) IMPORTANT STEP!!! Copy the env variables to crontab except DBUS_SESSION_BUS_ADDRESS.(WHY? Crontab uses it's own env variables ... no good.) 

	-> Type env > some_file. Remove DBUS_SESSION_BUS_ADDRESS line from the file. (Also remove such variable which are not assigned anything, if any)
	
	-> copy the whole text.
	
	-> type crontab -e ( A text file will open. Paste these env variable after the comments.
	
	-> If you know crontab now you can schedule to run the script.sh file as per your needs. For those who don't follow step 3.
	
	
3) Schedule crontab -
	-> Here what I write, will run the script every 10 minutes.
	-> 00,10,20,30,40,50 * * * * path-to-script/script.sh 
	-> type this in the file (crontab -e) and save and exit.
	-> For more info read man pages and the comments given above in crontab -e file.

Way 2 ----- DIY (Keep a while 1 starting at line 142/143 till the end and add this script in startup applications).

The script is well tested and has been run over the whole of the last semester without glitches. Still, if you have any problems please contact -
	->ayush.garg@students.iiit.ac.in
	->akshay.jaggi@students.iiit.ac.in



How to Check if the script is running or not ?

1) You can check the system logs for checking if the script ran or not. There
you will find lines like courses.py started, courses.py ended. Refer to the
program script for the same. You can add your own logs if you want.

2) Check if .Xdus file has been created in your home folder or not. (If using
crontab)

3) Check the folders are consistent with the information on portal.

4) The "data" file (shelve) is created in the directory where new_cour.py
script is present.


How to reset the script? (When sem changes.... or I change my courses or
password etc.)
-> You need to delete the "data" file from the folder where the script has run, then start the script manually once. If data file is not found it starts the script from the starting. 
