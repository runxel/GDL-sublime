# GDL-sublime
A bundle to make GDL available (meant as easy) in [Sublime Text](http://www.sublimetext.com/).

# What is GDL?
GDL means 'Geometric Description Language'. [ArchiCAD](http://www.graphisoft.com/) uses it to define a library part (it's also used internally for nearly everything).

Many users of ArchiCAD are making their own library parts. They are all tied to the – unfortunately horrible – build-in object editor which is stuck in the 80's or so. It doesn't even have line numbers!

But the rescue is ~~here~~ in the near future!
The purpose of this package is to comfortably write code in the best editor of the galaxy – Sublime Text! ;)

## Installation
Installation is not recommended at this time.
No, really! Do it at your own risk and only for testing, if you're sure what you're doing.

### ~~Using Sublime Package Control~~
_currently not available in your country. it will be later_

### Using Git
Alternatively you can install the bundle and keep up to date by cloning the repo directly into your `Packages` directory in the Sublime Text application settings area.

Go to your Sublime Text `Packages` directory and clone the theme repository using the command below:
`git clone https://github.com/runxel/GDL-sublime "GDL"`

### Download Manually
- Download the files using the GitHub .zip download option
- Unzip the files and rename the folder to 'GDL'
- Copy the folder to your Sublime Text `Packages` directory e.g. 
  - Windows `C:\Users\yourname\AppData\Roaming\Sublime Text 2\Packages\GDL`
  - OS X: `~/Library/Application Support/Sublime Text 2/Packages/GDL`

## Usage
From now on you can select 'GDL' as the current language in the bottom right corner of ST.

## Getting Started With Sublime Text
New to Sublime? Then I can recommend the excellent and free video tutorial by nettuts: [Perfect Workflow in Sublime Text](http://net.tutsplus.com/articles/news/perfect-workflow-in-sublime-text-free-course/).

## TO DO LIST
+ syntax implemention for 
	+ keywords for `REQUESTS`
	+ `WIDO_*, LABEL_*, LIGHT_*, WALL_*, COLU_*, BEAM_*, SLAB_*, ROOF_*, FILL_*, MESH_*`
+ usable and beatiful template

Goodies: 
+ Snippets
+ Tag completion
