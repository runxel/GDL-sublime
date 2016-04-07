# [GDL-sublime](https://github.com/runxel/GDL-sublime)
A bundle to make GDL available in [Sublime Text](http://www.sublimetext.com/).

[![Version](https://img.shields.io/badge/version-1.1.8-brightgreen.svg)]()

# What is GDL?
GDL means 'Geometric Description Language'. [ArchiCAD](http://www.graphisoft.com/) uses it to define a library part.

Many ArchiCAD users are making their own library parts, sell them or even publish them for free on sites like [BIMComponents](https://bimcomponents.com/), while others might modify the provided ones. But they are all tied to the – unfortunately horrible – build-in object editor which is stuck in the 80's or so. It doesn't even have line numbers!

But the rescue is here! _(at least something like that)_  
The purpose of this package is to give you the chance to comfortably write code in the best editor of the galaxy – Sublime Text.

This package provides **syntax highlighting** with a well aligned **color scheme** (aka syntax highlighting) and also **auto completion** (can be forced by pressing <kbd>ctrl</kbd> + <kbd>space</kbd>).

## Installation

### Using Sublime Package Control
_recommended_  
If you are using [Sublime Package Control](http://wbond.net/sublime_packages/package_control), you can easily install the bundle via the `Sublime Text -> Preferences -> Package Control: Install Package` menu item.

### Using Git
Alternatively you can install the bundle and keep up to date by cloning the repo directly into your `Packages` directory in the Sublime Text application settings area.

Go to your Sublime Text `Packages` directory and clone the repository using the command below:  
`git clone https://github.com/runxel/GDL-sublime "GDL"`

### Download Manually
_not recommended – you won't get updates!_  
- Download the files using the GitHub .zip download option
- Unzip the files and rename the folder to 'GDL'
- Copy the folder to your Sublime Text `Packages` directory e.g. 
  - Windows `C:\Users\yourname\AppData\Roaming\Sublime Text 2\Packages\GDL`
  - OS X: `~/Library/Application Support/Sublime Text 2/Packages/GDL`

## Usage
From now on you can select `GDL` as the current language in the bottom right corner of ST and enjoy all the benefits ST brings.  
But wait! There's more!
You should activate a the color scheme (=proper highlighting) by modifying the syntax specific preferences file, which you can find using the menu item `Preferences -> Settings - More -> Syntax Specific – User`, after you set the syntax to `GDL` for the current file.

There are 2 different color schemes at choice: A dark and a light one. _I muchly recommend the dark one for fatigue-proof coding!_

Copy _one_ of these into the new file and save:

#### **Dark:**
```json
{  
	"color_scheme": "Packages/GDL/GDL-dark.tmTheme"  
}
```

#### **Light:**
```json
{  
	"color_scheme": "Packages/GDL/GDL-light.tmTheme"  
}
```

#### Don't like the theme?
Don't worry. Go to the [ththeme-editor](http://tmtheme-editor.herokuapp.com/) and select one of the two themes as start and make one which satisfies you! (Note that the theme-editor of course has no preview for gdl code, so it's just direct scope color editing.)  
_See the [Wiki](https://github.com/runxel/GDL-sublime/wiki) for a list with the scopes so you can refine the scheme to suit your needs._  
Of course you could also edit the `.thTheme` files directly. Remember not to edit the provided one. Otherwise an update would overwrite your changes.

### Auto completion + Snippets
You may have to force the auto completion via <kbd>ctrl</kbd> + <kbd>space</kbd>.  
I have included some sample snippets. Try it out by typing in: `comline` and then press <kbd>TAB ↹</kbd>.  
Voilá! There's a divider.  
`! ---------------------------------------------------------------------- !`

I hardly encourage you to either modify the snippets, so they will suit your needs; or to make new ones.
You will find all the shipped snippets in the "Snippets" folder.

## Usage made even easier
This Sublime Text packages got accompanied by [GDLnucleus](http://www.opengdl.org/Default.aspx?tabid=9748) (_not free_). GDLnucleus is a assistant program which enables you to send your changes live to ArchiCAD from Sublime Text, instead of relying on copy+paste.
It can be understood as a SublimeText-project handler integrated with a link to the LP_XMLConverter, which comes with ArchiCAD. See the page for more details.
(_Please note: I did not made GDLnucleus._)

## Getting Started With Sublime Text
New to Sublime? Then I can recommend this excellent and free video tutorial by nettuts: [Perfect Workflow in Sublime Text](http://net.tutsplus.com/articles/news/perfect-workflow-in-sublime-text-free-course/).


### ~~TO DO LIST~~
