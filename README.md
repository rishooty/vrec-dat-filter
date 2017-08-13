# V's Recommended Dat Filter

This project was designed to solve a very niche problem for those who
aren't satisfied with the current state of building rom collections. 

As it stands one has two options: 
1. Obtain each rom you're interested in individually and slowly over time
2. Obtain complete romsets and sift through thousands of roms just to find or keep what you want.

So how does one optimize quality over quantity of roms in a short amount of time? 
For the most part this option hasn't existed. Until now.

V's Recommended Dat Filter is a set of python scripts and binaries that allow one to filter a dat file
to only the most likely desired games. It utilizes scrapy and [V's Recommended Wiki](http://vsrecommendedgames.wikia.com/wiki/) to get a list of
popular and highly recommended games for any platform, then creates a new dat file based on the results.
You can however, provide your own txt or csv lists as well.

For those feeling lazy, pre-cleaned and tweaked dats are provided [here](). (WIP)

## Getting Started

### Prerequisites

#### User

* Linux 32/64 distro with glibc 2.15+. Linux Mint and Ubuntu LTS are among these.
* Windows Vista 32/64 or higher.
* *Possible OSX Version in the Future*
* A dat file for the system you want to filter roms from.
    * [Consoles](http://datomatic.no-intro.org/) (Recommend "parent/clone xml" > "standard dat" for 1G1R.)
    * [Mame](http://www.progettosnaps.net/dats/)
* A rom manager clean to your roms with, all which usable in linux/osx with wine.
    * [ClrMamePro](https://mamedev.emulab.it/clrmamepro/)
    * [RomCenter](http://www.romcenter.com/) (4.x beta doesn't work with wine)
    * [Romulus](http://romulus.net63.net/)

#### Dev
* Python 3.5.x w/ virtualenv installed. You can go higher if you don't care about PyInstaller compatibility.
* The compiling essentials for your given os:
    * Debian/Ubuntu:
        ```
        sudo apt-get install build-essential
        ```
    * Windows: [Visual C++ Build Tools](https://www.visualstudio.com/downloads/#build-tools-for-visual-studio-2017)

### Setup

#### User
Download any of the following binaries:

[Linux 64-Bit](https://github.com/rishooty/vrec-dat-filter/raw/master/dist/vrec)

[Linux 32-Bit](https://github.com/rishooty/vrec-dat-filter/raw/master/dist/vrec)

[Windows 64-Bit](https://github.com/rishooty/vrec-dat-filter/raw/master/dist/vrec.exe)

[Windows 32-Bit](https://github.com/rishooty/vrec-dat-filter/raw/master/dist/vrec32.exe)

#### Dev
Simply download this repo and unzip, or 'git clone https://github.com/rishooty/vrec-dat-filter.git' to the directory of your choice.

1. First you need to create a virtualenv somewhere, preferably outside the repository:
    ```
    python(3.5) -m virtualenv ENV
    ```

2. Then you need to activate the environment you just created.

Under linux:

```
source ENV/bin/activate
```

Under Windows:
```
ENV/Scripts/activate.bat
```

3. Lastly, install all of the dependencies into your virtualenv
```
pip install -r requriements.txt
```

**Windows Only**

4. Download [Python for Windows Extensions](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/) that matches your build/run target. Then:
    ```
    python(3.5) -m easy_install <path to exe>
    ```
5. Finally, download and install [Windows 10 SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk). Then you'll need to copy every file from:
    ```
    C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64(or x32)\
    ```
    to:
    ```
    vRecScrape\dist
    ```
If you wish to use this with an ide, point the python interpreter to this project's virtualenv python binary.
For example, if you were using Pycharm Professional you'd set your project interpreter to:

```
...ENV/bin/python
```

## Running

Note: Initial executable depends on context.
*   Linux(user): ./vrec(32)
*    Linux(dev): ./Main.py
* Windows(user): vrec(32).exe
*  Windows(dev): python Main.py

That being said ignore the parentheses in the examples.

For more information on options, type -h after the executable or second argument.
```
(./vrec) (main) -h
```

### Main

In terminal, run:
```
(./vrec) main NES,Famicom 'testDat/Nintendo - Nintendo Entertainment System (20170719-133541).dat'
```

The name of the system you want to scrape for is the domain of that system's page. So in this example,
NES is derived from: http://vsrecommendedgames.wikia.com/wiki/NES.

Note the 'Famicom' after the main system name. This is a subsection of that same page. Oftentimes
v's breaks up subcategories of a console into tabs/subdomains. However, dat files are usually inclusive
of other regions and accessories. So to get around this, you'd add each section you want to include separated by commas.

In this instance, the no-intro NES dat file includes both American and Japanese regions. However, v's separates Japan(Famicom) into
it's own subsection.

### Scrape Only

This is for if you just want to generate a csv from V's. In this case all you would include is the system name(s):

```
(./vrec) scrape NES,Famicom
```

However, this script also includes a custom output path option. It will generate a
'listTemp.csv' in the project root by default.:
```
(./vrec) scrape NES,Famicom --path='recommendedNES.csv'
```

### Clean Only

This is for if you only need the dat cleaning functionality and wish to provide your own list of games to keep.
You can provide either a previous scraper generated csv, or a \n delimited textfile list. If none is provided,
it will just use the most recently generated 'listTemp.csv' by default.

```
(./vrec) clean 'testDat/Nintendo - Nintendo Entertainment System (20170719-133541).dat' --path='goodnesgames.txt'
```

A custom txt file would look something like this:
```
goodatarigames.txt
----------------------------
1943: The Battle of Midway
A Boy and His Blob: Trouble on Blobolonia
Abadox
....
```

### Directory Clean

This is functionality added as a workaround for when you can't quite find a good dat for your romset. This is both an option for 'main' and 'clean only',
as well as a standalone function.

This effectively performs the 'remove useless files' functionality of rom managers, but only on an exact name matching level. All it needs
is a cleaned dat file and a directory to filter roms from. When a file is found that isn't in your cleaned dat file, it's sent to recycle bin
rather than deleted. Still, **be very careful with this command**. That being said, use a rom manager if at all possible.

As an option:
```
(./vrec) main NES,Famicom' 'testDat/Nintendo - Nintendo Entertainment System (20170719-133541).dat' --rm_from='roms/nes/'
```

```
(./vrec) clean 'testDat/Nintendo - Nintendo Entertainment System (20170719-133541).dat' --path='goodnesgames.txt' --rm_from='roms/nes/'
```

As standalone:
```
(./vrec) dir_clean 'testDat/Nintendo - Nintendo Entertainment System (20170719-133541)clean.dat' 'roms/nes/'
```

### I've got my dat file, now what?
You're now ready to load it up into the rom manager of your choice and use it to clean out all non-matching roms.
This varies vastly between the rom managers. My personal favorite is RomCenter, so I will use it in my example.

0. **Backing up your roms is recommended**.

1. After opening up RomCenter, hit 'file->new->load games list from datafile'

2. Browse and select the cleaned dat. It should have the same name as the original, but with "clean" at the end.

3. Hit 'Create the game database', save the database with the default name.

4. It will now import, likely only taking a few seconds since the dat is much smaller.
    * If using romcenter 3.7.1, there's a rare bug that prevents certain dats from being read whether they're cleaned or not. In this case you may want to use the latest 4.0 beta.

5. Now hit the first toolbar button, a big yellow folder with a plus, to add the directory containing your roms. You can also drag and drop the folder onto the navigation window. I can't tell you where to get them, google is your friend, yadda yadda.

6. Hit the plus sign on rom files in the navigation window, highlight the first entry, and all roms matching the dat should be there.

7. Finally, hit 'arrow next to the toolbar wrench' or right click the rom folder entry you just highlighted, then 'remove useless files'. This will delete every rom that doesn't match your cleaned dat.
    * Before doing so, I recommend setting 'file->preferences->Romsets->check 1G1R box', but this will only work with parent/clone xmls or arcade related dats.

8. Your roms are now filtered! Note that:
    * Fuzzy matching isn't perfect, and there could be a few duplicates, false positives, or in very rare cases missing roms.
    * You can prevent the above by adding/removing these entries from the cleaned dat before heading to the rom manager. You can also set the --accuracy option to something higher or lower than 90.
    * You an also be lazy and delete/re-add these roms manually. After all, a couple stragglers is still an improvement over 1000's of roms.

### The latest dat doesn't work with my romset, what gives?
All too often dats will update faster than available romsets floating on the web. When this is the case with RomCenter 3.7.1,
hitting "remove useless files" will often delete most if not all the roms because it doesn't recognize them.

Now, getting an older dat would be the first thought that would occur to you. But the problem is that as soon as dats
are deprecated, they're almost effectively wiped from the internet and impossible to find, MAME being an exception.

It's for this reason I've added the 'dir_clean' functionality to this script, to get around this issue. It isn't a perfect solution, but
it gets the job done because oftentimes rom names stay the same and only checksums change. See Directory Clean section under Running.

## Compiling with PyInstaller
The cross platform quirks should be ironed out already in this repo, so compiling should be the same process for every os.

1. Access the virtualenv
    ```
    source ENV/bin/activate
    ```
    ```
    ENV/Scripts/activate.bat
    ```

2. Open Example.spec with a text editor, and change the following line as needed:
    ```
    datas=[('PATH_TO_ENV/Lib/site-packages/scrapy', 'scrapy')],
    ```

3. python -m PyInstaller Example.spec

It should produce a new executable for you to test your changes with.

## Built With

* [Python 3.5.2](https://www.python.org/) - Primary Language and common libraries.
* [PyPI/Pip](https://pypi.python.org/pypi)          - Dependency Management.
* [Scrapy](https://scrapy.org/)    - Used to generate lists of games from V's.
* [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy)           - Used to match dat entries against a list of games.
* [VirtualEnv](https://virtualenv.pypa.io/en/stable/)   - Used to condense and distribute this project for Devs.
* [PyInstaller](http://www.pyinstaller.org/)  - Used to condense and distribute this project for Users.
* [UPX 3.94](https://upx.github.io/) - Used in conjunction with PyInstaller to compress the executables.

## Author

**Nicholas Ricciuti** - [rishooty](https://github.com/rishooty)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* V's Recommended Wiki and all who contribute to it:
http://vsrecommendedgames.wikia.com/wiki/
* My coworker and mentor, Christopher Hill.
