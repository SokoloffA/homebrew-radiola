#!/usr/bin/env python3
# v 0.2

GITHUB_USER = "SokoloffA"
GITHUB_REPO = "radiola"
PROGRAM_NAME = "Radiola"

CASK_FILE = "Casks/radiola.rb"
#######################################
RELEASES_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases"


import sys
import urllib.request
import json
import re
import datetime
import hashlib

class Error(Exception):
    pass

class Version(tuple):
    def __init__(self, str) -> None:
        super().__init__()
        self = map(int, (str.split(".")))


def versiontuple(str):
    return tuple(map(int, (str.split("."))))


class Release:
    def __init__(self, data):
        self.tag = data["tag_name"]
        self.version = self.extractVersion(self.tag)
        self.prerelease = data["prerelease"]
        self.name = PROGRAM_NAME
        self.url = self.getUrl(data)
        self.changeLog = data["body"]
        self.date = datetime.datetime.strptime(data["published_at"], '%Y-%m-%dT%H:%M:%SZ')

    def extractVersion(self, tag):
        s = tag

        res = re.search(r"-beta\d+", s)
        if res:
            s = s[:res.start()]

        PREFIXES = [
            "v",
            "v.",
            f"{GITHUB_REPO}-",
        ]

        for p in sorted(PREFIXES, key=len, reverse = True):
            if s.startswith(p):
                s = s[len(p):]
                break

        if (re.match(r"[\d\.]+$", s)):
            return s

        raise Error(f"Can't extract version from '{tag}' tag")

    def getUrl(self, data):
        for asset in data["assets"]:
            if asset["browser_download_url"].endswith(".dmg"):
                return asset["browser_download_url"]

        return None

    @staticmethod
    def load():
        try:
            response = urllib.request.urlopen(RELEASES_URL)
            data = json.loads(response.read().decode('utf-8'))

            res = []
            for d in data:
                res.append(Release(d))

            return res
        except urllib.error.HTTPError as err:
            raise Error("Can't download from %s: %s" % (RELEASES_URL, err))


class Cask:
    def __init__(self):
        f = open(CASK_FILE, 'r')
        self.lines = f.readlines()
        f.close()
        self.version = None
        self.sha256  = None
        self.versionLine = None
        self.sha256Line = None

        n = -1
        for line in self.lines:
            n += 1
            line = line.strip()

            if not self.version and line.startswith("version"):
                self.versionLine = n
                self.version = line.split('"')[1]

            if not self.sha256 and line.startswith("sha256"):
                self.sha256Line = n
                self.sha256 = line.split('"')[1]


    def update(self, release):
        print(f"Release version: {release.version}")
        print(f"Cask version:    {self.version}")
        if release.version == self.version:
            print("Exit, no update required")
            return

        print(f"Update cask file")
        print(f"  * new version: {release.version}")

        response = urllib.request.urlopen(release.url)
        data = response.read()
        sha256 = hashlib.sha256(data).hexdigest()

        print(f"  * new hash:    {sha256}")

        self.lines[self.versionLine] = self.lines[self.versionLine].replace(self.version, release.version)
        self.lines[self.sha256Line] = self.lines[self.sha256Line].replace(self.sha256, sha256)

        f = open(CASK_FILE, 'w')
        for line in self.lines:
            f.write(line)
        f.close()


def getLast(releases):
    for r in releases:
        if not r.prerelease:
            return r

if __name__ == "__main__":

    try:
        releases = Release.load()
        release = getLast(releases)

        cask = Cask()
        cask.update(release)

    except Error as err:
        print("Error: %s" % err, file=sys.stderr)
