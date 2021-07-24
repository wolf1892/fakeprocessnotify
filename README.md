# fakeprocessnotify
Service/exe that creates fake process and alerts via email if killed. </br>


Simple python script that spawn fake process at root dir.
Heartbeat is sent to continously monitor the process, if the process is killed it alerts the User via Email (Canary)

Edit processname under array PROCESSES, you can further convert this to exe and push it as service. This makes sure, it is always under monitoring mode and user can get alerted if any malware tries to kill the process. 


Additional clenup required, not for production use.
