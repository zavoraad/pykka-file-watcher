import pykka, os, time, datetime, hashlib
from collections import deque

class FileWatcher(pykka.ThreadingActor):
        def __init__(self, fileStableActor, watchDirectory='./'):
                super().__init__()
                self.fileStableActor = fileStableActor
                self.watchDirectory=watchDirectory
                self.filesSeen = set()

        #
        # Return a list of new files that haven't been seen before
        #
        def determineNewFiles(self):
                allFiles = [self.watchDirectory + '/' + f for f in os.listdir(self.watchDirectory) if os.path.isfile(self.watchDirectory + '/' + f)]
                newFiles = set(set(allFiles) - set(self.filesSeen))
                return newFiles

        #
        # return files that are no longer 
        #
        def determineFilesNoLongerThere(self):
                allFiles = [self.watchDirectory + '/' + f for f in os.listdir(self.watchDirectory) if os.path.isfile(self.watchDirectory + '/' + f)]
                return set(set(self.filesSeen) - set(allFiles))

        #
        # interval is a time in seconds to check the directory for new files
        #
        def watch(self, interval=5):
                while True:
                        newFiles = self.determineNewFiles()
                        #tell new files
                        if len(newFiles) > 0:
                                print('new files I have seen are: ' + str(newFiles))
                                try:
                                        self.fileStableActor.tell(newFiles)
                                except Exception as e:
                                        print(str(e))
                        self.filesSeen = set(self.filesSeen - self.determineFilesNoLongerThere())
                        self.filesSeen = self.filesSeen.union(newFiles)
                        time.sleep(interval)

#
# Helper class used to compare files
#
class FileDetails():
        def __init__(self, fileLocation):
                self.fileLocation = fileLocation
                self.fileMD5 = hashlib.md5(open(self.fileLocation,'rb').read()).hexdigest()
                self.timestamp = datetime.datetime.now().timestamp() 

        #
        # Determine if the file is the same in name and md5
        #
        def __eq__(self, obj):
                 return isinstance(obj, FileDetails) and obj.fileLocation == self.fileLocation and obj.fileMD5 == self.fileMD5

class FileStableManager(pykka.ThreadingActor):
        def __init__(self):
                super().__init__()

        #
        # recieves location of files as a set
        #
        def on_receive(self, message):
                try:
                        print('FileStableManager received this message ' + str(message))
                        if isinstance(message, set):
                                #this is a set of new files, lets see if they are stable
                                print('Checking to see if this file is stable in FileStableManager ' + str(message))
                                fileStable = [FileStable.start(self.actor_ref) for _ in range(len(message))]
                                for i in range(len(message)):
                                        print('calling the FileStable actor with input ' + list(message)[i])
                                        fileStable[i].tell(list(message)[i])
                        elif isinstance(message, FileDetails):
                                #TODO this is a stable file, time to process it
                                print('TOD passing off to the next actor to process as this file is stable ' + str(message.fileLocation))
                except Exception as e:
                        print(str(e))

        #
        # determine if the actor dies and print stacktrace
        #
        def on_failure(exception_type, exception_value, traceback):
                print('actor died')
                print(exception_type + ':' + exception_value + ':' + traceback)

#
# Tell 
# 
class FileStable(pykka.ThreadingActor):
        def __init__(self, fileStableManager, minutes=1):
                super().__init__()
                self.time=datetime.datetime.now()
                self.fileStableManager = fileStableManager
                self.minutes=minutes

        #
        # message of type fileDetails
        #
        def on_receive(self, message):
                try:
                        print('I received a message in FileStable')
                        self.isStable(fileDetails = FileDetails(message))
                except Exception as e:
                        print(str(e))

        #
        # method to check if a file is stable for self.minutes
        #
        def isStable(self, fileDetails):
                print('FileStable actor started and is checking to make sure file is stable ' + fileDetails.fileLocation)
                while True:
                        if fileDetails == FileDetails(fileDetails.fileLocation):
                                if  ((datetime.datetime.now() - self.time).total_seconds() / 60) > self.minutes:
                                        print('was able to determine file was stable ' + str(fileDetails.fileLocation) + ' for the given minutes ' + str(self.minutes))
                                        self.fileStableManager.tell(fileDetails)
                                        self.actor_ref.stop()
                        else:
                                fileDetails = FileDetails(fileDetails.fileLocation)
                                self.time=datetime.datetime.now()
                                time.sleep(60 * self.minutes)
#
# Look for files in the current directory, ./
#
if __name__ == '__main__':
        stableManager = FileStableManager.start()
        watcher = FileWatcher.start(fileStableActor=stableManager, watchDirectory='./').proxy()
        watcher.watch(interval=5)
