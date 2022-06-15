# Sample File Transfer Watcher Implemented in Python & Pykka

## Description
In this program exploring the functionality of akka actor model programming. Taking advantage of multi-threaded actors, divide and conquer of tasks, and mailbox messaging to simplify how to identify new files (potentially being trasnferred or copied) to be picked up and processed. Program written mostly for educational purposes

## Workflow 
FileWatcher (watches for new files appearing in directory maintaining internal state of fileList). new file TELL<br/>
&ensp;FileStable -> (determine that a file is stable, e.g. no longer being copied to location based upon file size and interval). file is steady TELL<br/>
&ensp;&ensp;N/A -> This is where we leave off for [furuther processing] https://github.com/zavoraad/pykka-file-watcher/blob/26ee7ae1cc9a58e0382ff602889a5957e00ed0fd/sample.py#L75-L77

## Example

