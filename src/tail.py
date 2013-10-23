import os, os.path, subprocess, time, threading, functools, json, urllib2, uuid, sys, itertools
from functools import partial

class FileNotFoundException(Exception): pass

subprocesses = []

class Tail(object):

	STATUS_INIT = "init"
	STATUS_RUNNING = "running"
	STATUS_STOPPED = "stopped"
	STATUS_ERROR = "error"
	STATUS_FINISHED = "finished"

	TAIL_INIT_TIME = 0.2 # second(s)
	WAIT_FILE_EXIST_TIME = 0.2 # second(s)

	def __init__(self, fileName):
		self.fileName = fileName
		self.status = self.STATUS_INIT
		self.tailProcess = None

	def run(self):
		if self.status != self.STATUS_INIT:
			raise Exception("must be in %s state to call start method" % self.STATUS_INIT);
		self.status = self.STATUS_RUNNING
		self.waitForFileExist()			
		self.tailProcess = subprocess.Popen(['tail','-F',self.fileName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		while self.isRunning():
			try:
				self.tailProcess.poll()
				if self.tailProcess.returncode == 1: 
					# FileNotFound
					continue
				elif self.tailProcess.returncode != None: 
					# "weird error :("
					self.status = self.STATUS_ERROR
				else:
					line = self.tailProcess.stdout.readline()[:-1]
					if line != "": 
						self.processLine(line)
			except Exception as e:
				self.status = self.STATUS_STOPPED
				import traceback
				traceback.print_exc(file=sys.stdout)
		self.kill()
		return self
		
	def processLine(self, line):
		raise Exception('not implemented')

	def stop(self):
		if self.status == self.STATUS_RUNNING:
			self.status = self.STATUS_STOPPED
		return self

	def kill(self):
		if self.tailProcess == None: return
		self.tailProcess.poll()
		if self.tailProcess.returncode == None:
			try:
				self.tailProcess.kill()
			except Exception:
				self.kill()	
		return self

	def waitForFileExist(self):
		while self.isRunning() and not os.path.exists(self.fileName):
			time.sleep(self.WAIT_FILE_EXIST_TIME)
		return self

	def isRunning(self): return self.status == self.STATUS_RUNNING


class ThreadTail(Tail):

	def __init__(self, fileName):
		super(ThreadTail, self).__init__(fileName)
		self.worker = threading.Thread(target=self.run)
		self.worker.daemon = True

	def start(self):
		self.worker.start()
		return self

	def join(self):
		self.worker.join()
		return self

	def stopThread(self):
		super(ThreadTail, self).stop()
		return self.join()

class Config(object):

	def __init__(self, fileName):
		self.fileName = fileName

	def getConfig(self):
		if hasattr(self, "config"):
			return self.config
		self.config = self.loadConfigFromDefault()
		if self.fileName and os.path.exists(self.fileName):
			try:
				config = self.loadConfigFromFile()
				assert "apiKey" in config
				assert "address" in config
				assert "files" in config
				self.config = config
			except Exception, e:
				print >>sys.stderr, "unable to load from file '%s' because '%s'. using defaults" % (self.fileName, e)
		self.saveConfig()
		self.config["files"] = { os.path.abspath(f): c for f,c in self.config["files"].items() }
		return self.config

	def getAddress(self):
		return self.getConfig()["address"]

	def getApiKey(self):
		return self.getConfig()["apiKey"]

	def getFiles(self):
		return self.getConfig()["files"].keys()

	def getChannel(self, fileName):
		return self.getConfig()["files"][fileName]

	def saveConfig(self):
		with open(self.fileName, "w+t") as handle:
			handle.write(json.dumps(self.getConfig()))
		return self

	def loadConfigFromDefault(self):
		return {
			"apiKey": "someApiKey",
			"address": "http://192.168.2.158:1025",
			"files": {
				"log1.txt": "hello",
				"log2.txt": "hello"
			}
		}

	def loadConfigFromFile(self):
		if not os.path.exists(configFileName):
			exit(1)

		with open(configFileName) as configHandler:
			return json.loads(configHandler.read())

class DebugChannelTail(ThreadTail):

	def __init__(self, config, *args, **kwargs):
		super(DebugChannelTail, self).__init__(*args, **kwargs)
		self.macAddress = self.getMacAddress()
		self.sequenceNumbers = itertools.count()

	def processLine(self, line):
		print ">>>> " + line
		headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'User-Agent': "Mozilla/5.0"} 
		req = urllib2.Request(
			config.getAddress() + "/" + config.getChannel(self.fileName),
			json.dumps({
				"handler": "tail", 
				"args": [self.fileName, line],
				'info': {
					'pid': os.getpid(),
					'machineId': self.macAddress,
					'generationTime': time.time(),
					'sequenceNo': self.sequenceNumbers.next()
				}
			})
		)
		map(lambda (x,y): req.add_header(x,y), headers.items())
		urllib2.urlopen(req)

	@staticmethod
	def getMacAddress():
		return ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])

configFileName = os.path.join(os.path.expanduser("~"),".tail.json")
config = Config(configFileName)
tails = map(lambda f: DebugChannelTail(config, f).start(), config.getFiles())
try:
	map(lambda t: t.join(), tails)
except KeyboardInterrupt:
	map(lambda t: t.stopThread(), tails)
exit(0)