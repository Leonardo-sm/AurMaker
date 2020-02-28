import sys
import os
import time
import argparse
import requests
import subprocess
from bs4 import BeautifulSoup

class ExtendAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or []
        items.extend(values)
        setattr(namespace, self.dest, items)

def download(link):
    print(link)
    on = os.system("wget " + link)
    if on != 0:
       return "Programa nao encontrado"
    else:
        return "Dowlod Completo"

def linkMaker(programs):
    program = programs + ".tar.gz"
    urlMount = urlBase + program
    return urlMount

def unzip(program):
    programTar = program + ".tar.gz"
    os.system("tar -xvf " + programTar)
    return 0

def maker(program):

    res = (str(subprocess.check_output("echo $HOME", shell=True)))
    r = res.split("'")
    pat = r[1]
    p = pat.split("\\")
    home = p[0]
    
    path = home + "/" + "Downloads/" + program + "/"
    os.chdir(path)
    time.sleep(0.5)
    log = os.system("makepkg -si")
    return log

def takeVersion(version):
    req = requests.get(version)
    if req.status_code == 200:
        content = req.content
        soup = BeautifulSoup(content, "html.parser")
        title = soup.findAll(name="h2")
        t = title[1]
        t  = str(t)
        t = t.split(" ")
        v = t[3].split("<")
        version = v[0]
        return version
    else:
        print("Programa nao encontrado")

def compare(items, progs):
    res = (str(subprocess.check_output("export | grep 'HOME'", shell=True)))
    r = res.split('"')
    pathUser = (r[1])
    pv = ""
    for prog in progs:
        pv += prog + " "
    
    os.system("pacman -Qm " + pv + "> /$HOME/.aurmaker/versions/version.txt")
    file = open(pathUser + "/.aurmaker/versions/version.txt", "r")
    i = 0

    for line in file:
        ver = line.split(" ")
        v = ver[1].rstrip("\n")
        item = items[i]
        i += 1
        print(item," ", line)
        if item != v:
            toUpdate.append(ver[0])
        else:
            print("ja esta na ultima versao.")
    return 0

home = os.system("echo $HOME")

urlBase = "https://aur.archlinux.org/cgit/aur.git/snapshot/"

parser = argparse.ArgumentParser()
parser.register("action", "extend", ExtendAction)
parser.add_argument("-S", nargs="+", action="extend", dest="progInstall")
parser.add_argument("-R", nargs="+", action="extend", dest="progUnstall")
parser.add_argument("-Qi", nargs="+", action="extend", dest="progInfo")
parser.add_argument("-Sya", nargs="+", action="extend", dest="progVersion")

args = parser.parse_args()

progNamesUnstall = args.progUnstall
programsNames = args.progInstall
programsInfo = args.progInfo
programsVersion = args.progVersion
links = []

if programsNames != None:
    for program in programsNames:
        program = program.lower()
        url = linkMaker(program)
        links.append(url)

    for link in links:
        downloadComplet = download(link)
        print(downloadComplet)

    for progZip in programsNames:
        unzip(progZip)

    for progInstall in programsNames:
        log = maker(progInstall)
elif progNamesUnstall != None:
    for progUnstall in progNamesUnstall:
        os.system("sudo pacman -R " + progUnstall)
elif programsInfo != None:
    if programsInfo[0] != "All":
        for progInfo in programsInfo:
            os.system("pacman -Qi " + progInfo)
    else:
        os.system("pacman -Qi")

elif programsVersion != None:
    version = []
    toUpdate = []
    for progV in programsVersion:
        url = "https://aur.archlinux.org/packages/"
        url += progV + "/" 
        version.append(takeVersion(url))
    compare(version, programsVersion)
    print(toUpdate)
    if toUpdate != None:
        for program in toUpdate:
                program = program.lower()
                url = linkMaker(program)
                links.append(url)

        for link in links:
            downloadComplet = download(link)
            print(downloadComplet)
        
        for progZip in toUpdate:
            unzip(progZip)

        for progInstall in toUpdate:
            log = maker(progInstall)

else:
    print("Digite aurmaker -h para ver como usar o programa")
