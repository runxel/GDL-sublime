# GDL-sublime
A bundle to make GDL available ("available" as in "easy" :D) in [Sublime Text](http://www.sublimetext.com/).

# What is GDL?
GDL means 'Geometric Description Language'. [ArchiCAD](http://www.graphisoft.com/) uses it to define a library part (it's also used internally for nearly everything).

Many users of ArchiCAD are making their own library parts or even publish them on [BIMComponents](https://bimcomponents.com/). But they are all tied to the – unfortunately horrible – build-in object editor which is stuck in the 80's or so. It doesn't even have line numbers!

But the rescue is here! _(at least something like that)_  
The purpose of this package is to comfortably write code in the best editor of the galaxy – Sublime Text! ;)

This package provides syntax highlighting together with a well aligned color and also auto completion. (Can be forced by pressing `ctrl + space`)

## Installation

### Using Sublime Package Control
*recommended*  
If you are using [Sublime Package Control](http://wbond.net/sublime_packages/package_control), you can easily install the bundle via the `Sublime Text -> Preferences -> Package Control: Install Package` menu item.

### Using Git
Alternatively you can install the bundle and keep up to date by cloning the repo directly into your `Packages` directory in the Sublime Text application settings area.

Go to your Sublime Text `Packages` directory and clone the repository using the command below:  
`git clone https://github.com/runxel/GDL-sublime "GDL"`

### Download Manually
- Download the files using the GitHub .zip download option
- Unzip the files and rename the folder to 'GDL'
- Copy the folder to your Sublime Text `Packages` directory e.g. 
  - Windows `C:\Users\yourname\AppData\Roaming\Sublime Text 2\Packages\GDL`
  - OS X: `~/Library/Application Support/Sublime Text 2/Packages/GDL`

## Usage
From now on you can select `GDL` as the current language in the bottom right corner of ST and enjoy all the benefits ST brings.  
But wait! There's more!
Activate a well aligned color scheme by modifying the syntax specific preferences file, which you can find using the menu item `Preferences -> Settings - More -> Syntax Specific – User`, after you set the syntax to `GDL` for the current file.

Copy this into the new file and save:
`{  
	"color_scheme": "Packages/GDL/GDL.tmTheme"  
}`

### Auto completion + Snippets
You may have to force the auto completion via `ctrl + space`.  
Also some Snippets are now on board. Try it out! Type in: `comline` and then press TAB.  
Voilá! There's a divider.  
`! ---------------------------------------------------------------------- !`


## Getting Started With Sublime Text
New to Sublime? Then I can recommend the excellent and free video tutorial by nettuts: [Perfect Workflow in Sublime Text](http://net.tutsplus.com/articles/news/perfect-workflow-in-sublime-text-free-course/).

## TO DO LIST
