[![radiola](radiola.png)](https://github.com/SokoloffA/radiola)
# homebrew-radiola
Install Radiola via Homebrew

The program has not currently reached the popularity threshold for inclusion in the official homebrew repositories. You can help by giving the [Radiola](https://github.com/SokoloffA/radiola) project a star and/or start a watch.

Right now you can use my *Tap* to install the program using homebrew.


## Installation

First, make sure you have installed [`homebrew`](https://brew.sh) if you haven't yet.

Then add radiola tap. You only need to do this once.
```
$ brew tap sokoloffa/radiola
```

Install the program
```
$ brew install --cask --no-quarantine radiola
```
*Why you need the **"--no-quarantine"** parameter?  
MacOS marks all files downloaded from the Internet as quarantined. When you run a quarantined program, OS displays the message **«Radiola can’t be opened because Apple cannot check it for malicious software"**.
Of course, the new program is downloaded from the Internet, so don't mark it as quarantined use the **"--no-quarantine"** option*.

## Uninstall

Run the following:
```
$ brew uninstall --cask radiola
```
