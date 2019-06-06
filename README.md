# [GDL-sublime](https://github.com/runxel/GDL-sublime)
A bundle to make GDL available in [Sublime Text](http://www.sublimetext.com/).

[![Version](https://img.shields.io/github/release/runxel/GDL-sublime.svg?style=flat-square)](https://github.com/runxel/GDL-sublime/releases/latest)

![dark color scheme](https://i.imgur.com/OEurk9A.png)  

# What is GDL?
GDL means 'Geometric Description Language'. [ArchiCAD](http://www.graphisoft.com/) uses it to define a library part.

Many ArchiCAD users are making their own library parts, sell them or even publish them for free on sites like [BIMComponents](https://bimcomponents.com/), while others just want to modify the provided ones. But they are all tied to the – unfortunately horrible – built-in object editor which is stuck in the 80's or so. It doesn't even have line numbers!

But salvation is here!  
The purpose of this package is to give you the chance to comfortably write code in the best editor of the galaxy – [Sublime Text](https://www.sublimetext.com/).

This package provides the whole thing: from **syntax highlighting** (with a well aligned **color scheme**) to **auto completion**, **global goto**, **snippets**, and last but not least a **build system** for your scripts.

## Installation

### Using Sublime Package Control
:white_check_mark: _recommended_  
If you are using [Sublime Package Control](http://wbond.net/sublime_packages/package_control), you can easily install the bundle via the `Sublime Text -> Preferences > Package Control: Install Package` menu item.

### Using Git
:robot: Alternatively you can install the bundle and keep up to date by cloning the repo directly into your `Packages` directory in the Sublime Text application settings area.

Go to your Sublime Text `Packages` directory and clone the repository using the command below:  
`git clone https://github.com/runxel/GDL-sublime "GDL"`

### Download Manually
:arrow_down: _not recommended – you won't get updates!_ :rotating_light:  
- Download the files using the GitHub .zip download option
- Unzip the files and rename the folder to 'GDL'
- Copy the folder to your Sublime Text `Packages` directory i.e. 
  - Windows `C:\Users\<yourname>\AppData\Roaming\Sublime Text 3\Packages\GDL`
  - OS X: `~/Library/Application Support/Sublime Text 3/Packages/GDL`

## Usage
From now on you can select `GDL` as the current language in the bottom right corner of ST and enjoy all the benefits. For files with the `.gdl` extension it will be automatically active.  
For the coloring (meaning the proper highlighting) there are two choices. By default a light color scheme will be applied.  
I personly like the dark coloring more providing fatigue-proof coding. To change the use of a color scheme go to `Preferences > Package Settings > GDL > Settings`.  

Copy _one_ of these into the file on the right and save:

#### **Dark:**
```json
{  
	"color_scheme": "Packages/GDL/GDL-dark.sublime-color-scheme"  
}
```

#### **Light:**
```json
{  
	"color_scheme": "Packages/GDL/GDL-light.sublime-color-scheme"  
}
```
![light color scheme](https://i.imgur.com/OQx2IF2.png)  

#### Don't like the theme?
You can edit the `.sublime-color-scheme` files directly. But remember to copy and rename the provided one. Otherwise an update would overwrite your changes.

### GoTo, Auto completion, Snippets
The "Goto" feature of Sublime Text is pretty powerful. To gain full access you must use [Sublime projects](#workflow). If you e.g. quickly want to got to a subroutine place your cursor into the name and press <kbd>F12</kbd>. You will then jump directly to the definition.  
Auto completion takes place automatically, if you're typing. You can force auto completion via <kbd>ctrl</kbd> + <kbd>space</kbd>.  
I have included some example snippets. Try it out by typing in: `comline` and then press <kbd>TAB ↹</kbd>.  
Voilá! There's a divider.  
`! ---------------------------------------------------------------------- !`

I hardly encourage you to modify and extend the snippets, so they will suit your needs.  
You will find all the shipped snippets in the `Snippets` folder.

## Workflow
With the advent of ARCHICAD 23 we don't longer need third-party apps like [GDLnucleus](http://www.opengdl.org/Default.aspx?tabid=9748) for a Sublime Text driven workflow. The **LP_XMLConverter**, which is part of every Archicad installation, can now convert `.gsm` directly into subsequent `.gdl` scripts and vice-versa. This means an end to the abundant copy & pasting orgy of the past.  

To use this feature you first need to set the path to where your ARCHICAD is installed. Open the package settings again, with the pencil icon on the left you can copy the respective item from the left to the right pane. Change the path accordingly.  
Afterwards drag and drop a folder with your 'gsm' (I recommend different folders for different gsm's) into Sublime Text and then create a Sublime project via `Project > Save Project sAs…`. Other benefits are a better working 'goto', 'auto completion', and the possibility to fast switch between different coding sessions on various gsm's.  
You can now use the the two conversion options in `Tools > GDL`. For a quick access both items are reachable via a right mouse click on the editor pane and key bindings on each.  
The default for `Convert to script (gsm ⯈ hsf/gdl)` is <kbd>ctrl</kbd>+<kbd>shift</kbd>+<kbd>H</kbd>. `Build GSM from HSF (hsf/gdl ⯈ gsm)` has <kbd>ctrl</kbd>+<kbd>shift</kbd>+<kbd>alt</kbd>+<kbd>G</kbd>. Of course this can be adjusted to your taste.  
&nbsp;
![cmd args](https://i.imgur.com/HDiunZe.png)
&nbsp;
If you need to provide additional arguments for the LP_XMLConverter, you can do so by `Project > Edit Project`, then copy this into the open file:
```json
"cmdargs":
{
    "to-hsf": "<args>",
    "to-gsm": "<args>"
}
```
where `<args>` is to be replaced. If you don't need it, you can leave it empty. To check the possible args you can run the LP_XMLConverter with the `-?` argument to get help.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

## Getting Started With Sublime Text
New to Sublime? Then I can recommend this excellent and free video tutorial by nettuts: [Perfect Workflow in Sublime Text](http://net.tutsplus.com/articles/news/perfect-workflow-in-sublime-text-free-course/).

## Support
Does this plugin help you in your daily work, or just want to say thanks?  
Please consider donating to sustain working on this plugin.

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y5VOOM)

[![Beerpay](https://beerpay.io/runxel/GDL-sublime/badge.svg?style=beer-square)](https://beerpay.io/runxel/GDL-sublime)
