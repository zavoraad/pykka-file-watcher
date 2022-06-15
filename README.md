# Sample File Transfer Watcher Implemented in Python & Pykka

## Description
In this program exploring the functionality of akka actor model programming. Taking advantage of multi-threaded actors, divide and conquer of tasks, and mailbox messaging to simplify how to identify new files (potentially being trasnferred or copied) to be picked up and processed. Program written mostly for educational purposes. 

## Workflow 
*FileWatcher* (watches for new files appearing in directory maintaining internal state of fileList). new file TELL <br/>
&ensp;*FileStable* -> (determine that a file is stable, e.g. no longer being copied to location based upon file size and interval of 1 minute by default). file is steady TELL<br/>
&ensp;&ensp;N/A -> This is where we leave off for [furuther processing] https://github.com/zavoraad/pykka-file-watcher/blob/26ee7ae1cc9a58e0382ff602889a5957e00ed0fd/sample.py#L75-L77

## Example
Running this file watcher on this Github repo's files
```bash
$ pip install -r requirements.txt && python sample.py 
```
> new files I have seen are: {'.//requirements.txt', './/LICENSE', './/README.md', './/sample.py'}<br/>
FileStableManager received this message {'.//requirements.txt', './/LICENSE', './/README.md', './/sample.py'}<br/>
Checking to see if this file is stable in FileStableManager {'.//requirements.txt', './/LICENSE', './/README.md', './/sample.py'}<br/>
calling the FileStable actor with input .//requirements.txt<br/>
calling the FileStable actor with input .//LICENSE<br/>
I received a message in FileStable<br/>
calling the FileStable actor with input .//README.md<br/>
calling the FileStable actor with input .//sample.py<br/>
I received a message in FileStable<br/>
I received a message in FileStable<br/>
I received a message in FileStable<br/>
FileStable actor started and is checking to make sure file is stable .//requirements.txt<br/>
FileStable actor started and is checking to make sure file is stable .//sample.py<br/>
FileStable actor started and is checking to make sure file is stable .//LICENSE<br/>
FileStable actor started and is checking to make sure file is stable .//README.md<br/>
was able to determine file was stable .//LICENSE for the given minutes 1<br/>
FileStableManager received this message <__main__.FileDetails object at 0x10c93c070><br/>
TODO passing off to the next actor to process as this file is stable .//LICENSE<br/>
was able to determine file was stable .//requirements.txt for the given minutes 1<br/>
FileStableManager received this message <__main__.FileDetails object at 0x10c80f0d0><br/>
TODO passing off to the next actor to process as this file is stable .//requirements.txt<br/>
was able to determine file was stable .//README.md for the given minutes 1<br/>
FileStableManager received this message <__main__.FileDetails object at 0x10c93f7f0><br/>
was able to determine file was stable .//sample.py for the given minutes 1<br/>
TODO passing off to the next actor to process as this file is stable .//README.md<br/>
FileStableManager received this message <__main__.FileDetails object at 0x10c93f7c0><br/>
TODO passing off to the next actor to process as this file is stable .//sample.py<br/>
