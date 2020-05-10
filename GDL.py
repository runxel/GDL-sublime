# -*- coding: utf-8 -*-

import os
import sublime
import sublime_plugin
import sys
import logging

log = logging.getLogger(__name__)

PACKAGE_SETTINGS = "GDL.sublime-settings"
DEFAULT_AC_PATH = "C:/Program Files/GRAPHISOFT/ARCHICAD 23"
DEFAULT_AC_PATH_MAC = "/Applications/GRAPHISOFT/AC23/ARCHICAD 23.app"

def save_all_files():
	""" Saves all files open in Sublime.
		Mimics the 'save on build' behavior of Sublime Text.
	"""
	for window in sublime.windows():
		for view in window.views():
			if view.file_name() and view.is_dirty():
				view.run_command("save")

def get_project_settings(view, request, *args):
	""" Returns the requested parameters from the `.sublime-project` file.
		If the the very parameter does not exist this method return an empty string.
		TODO: migrate all other functions to this one
	"""
	project_data = view.window().project_data()

	if not project_data:
		err("You must create a project first! (Project > Save Project As...)")
		return

	project_settings = project_data.get(request, "")

	return project_settings

def get_project_data(view, invoke):
	""" Gets the data of the .sublime-project file.
		Returns additional arguments for the commandline operation,
		if the user has set any.
	"""
	# invoke options: 'to-hsf' / 'to-gsm' / 'proj_gsm_path'
	project_data = view.window().project_data()
	if not project_data:
		err("You must create a project first! (Project > Save Project As...)")
		return

	project_settings = project_data.get('cmdargs', {})
	if type(project_settings) is dict:
		# check if dict is empty
		if bool(project_settings):
			return project_settings.get(invoke, "")
		else:
			# dict is empty, which means user hasn't set any cmdargs
			return ""
	else:
		err()
		return

def get_project_subroot(view):
	""" Gets the data of the .sublime-project file.
		Returns a relative path, if set.
		(Useful, if you have many subfolders and want to assign
		a new root, where all the objects are in.)
	"""
	project_data = view.window().project_data()
	sub_root_setting = project_data.get('root', "")
	return sub_root_setting

def get_ac_path(view, pckgset):
	""" Returns a path to a certain Archicad version, either from project file or the global settings.
		(Former is useful if one is developing for different Archicad versions and
		they want to use the appropiate LP Converter version.)
	"""
	proj_ac_path = get_project_settings(view, "AC_path")

	if not proj_ac_path:
		ac_path = str(pckgset.get("AC_path", DEFAULT_AC_PATH))
	else:
		ac_path = proj_ac_path
		
	return ac_path

def err(text):
	""" Gives us a ST error message. """
	if not text:  # None or empty
		text = "Sorry. Something went wrong."
	sublime.error_message(text)

def is_dir(*args):
	""" Takes arguments and determines if the resulting path is a directory. """
	try:
		is_dir = os.path.isdir(os.path.join(*args))
	except:
		is_dir = False
	return is_dir

def is_file(*args):
	""" Takes arguments and determines if the resulting path is a file. """
	try:
		is_file = os.path.isfile(os.path.join(*args))
	except:
		is_file = False
	return is_file

def splitall(path):
	""" Returns all parts of a path as a list. """
	allparts = []
	while 1:
		parts = os.path.split(path)
		if parts[0] == path:  # sentinel for absolute paths
			allparts.insert(0, parts[0])
			break
		elif parts[1] == path: # sentinel for relative paths
			allparts.insert(0, parts[1])
			break
		else:
			path = parts[0]
			allparts.insert(0, parts[1])
	return allparts


class GdlOnSave(sublime_plugin.EventListener):
	""" Establishes an event listener, which gets active when the user saves a GDL file.
		If the appropiate setting is set, a GSM will be built automatically.
	"""
	def on_post_save_async(self, view):
		# check if the project has the setting
		if view.window().project_data().get("convert_on_save", False):
			# only get active when the user edited a GDL file
			if view.match_selector(0, "source.gdl"):
				view.window().run_command('libpart_build', {"on_post_save_state": True})


############################################################################
class Builder(sublime_plugin.WindowCommand):
	def run(self, *args, **kwargs):
		self.view = self.window.active_view()
		self.pckg_settings = sublime.load_settings(PACKAGE_SETTINGS)
		
		# get the path to the LP_XML_Converter right
		self.AC_path = get_ac_path(self.view, self.pckg_settings)

		self.lp_conv_path = self.check_system()
		self.converter = os.path.join(self.AC_path, self.lp_conv_path)

		if self.view.settings().get("auto_save", True):
			save_all_files()

		if self.on_post_save_state:
			# if coming from the on_post_save event listener we can directly proceed without selection
			self.delegator()
		else:
			self.selection_process()

	def selection_process(self):
		# determine if there is a sub root folder being set in the project settings
		self.sub_root_path = get_project_subroot(self.view)
		if self.sub_root_path:  # empty str are falsy
			self.has_subroot = True
			_debug_subroot = self.sub_root_path
		else:
			self.has_subroot = False
			_debug_subroot = "<not set>"
		log.debug("Sub-Root Path is: {}".format(_debug_subroot))

		if len(self.window.folders()) > 1:
			err("You can't use the GDL-Sublime plugin as a menu command in a multi root environment.\n"
				"Please try the 'convert_on_save' setting instead.\n"
				"Alternatively you might be able to rearrange your folder structure to use the 'sub root' setting.")
			return

		if len(self.window.folders()) > 1 and self.sub_root_path:
			# this means there are multiple folders linked into ST
			# there would be an ambiguity for which of the folders the `root` feature should apply
			err("You can not use the 'root' setting in a multiroot environment.\n"
				"Maybe try the 'convert_on_save' setting.")
			return
		if len(self.window.folders()) > 1:
			self.has_multi_root = True
		else:
			self.has_multi_root = False

		self.project_abs_basepath = self.window.folders()

		# get the list of folders which could be part of a conversion
		self.folders = self.get_folders()
		log.debug("Folders prior to selection: {}".format(self.folders))

		if len(self.folders) <= 0:
			err("GDL build command error: Please open a project, or.\n"
				"make sure all folders and files are named properly.\n"
				"If in doubt consult the README.")
		elif len(self.folders) == 1:
			self.has_multiple_folders = False
			self.working_dir = self.folders[0]
			self.delegator()
		else:
			self.has_multiple_folders = True
			self.pick_working_dir(self.folders)

	def check_system(self):
		""" Returns the path to the LP_XML converter.
		"""
		if sys.platform.startswith('darwin'): # OSX
			self.os_win = False
			return "Contents/MacOS/LP_XMLConverter.app/Contents/MacOS/LP_XMLConverter"
		elif sys.platform.startswith('win'):  # Windows
			self.os_win = True
			return "LP_XMLConverter.exe"
		else:
			err("GDL build error: Your OS is not supported.")
			return

	def get_folders(self):
		""" Retrieves all subfolders of the working directory and returns
			a subset which includes all valid items as a list.
		"""
		if self.has_subroot:  
			abs_path_with_subroot = os.path.join(self.project_abs_basepath[0], self.sub_root_path)
			# first let's check if user has linked to a object folder directly
			# we can answer that by checking if there is an appropiate GSM or folder directly in the directory
			rootbase = os.path.basename(os.path.normpath(abs_path_with_subroot))
			if is_dir(abs_path_with_subroot, rootbase) or is_file(abs_path_with_subroot, rootbase +'.gsm'):
				folders = [abs_path_with_subroot]
			else:
				folders = self.valid_subfolders(abs_path_with_subroot)
		else:
			# get all the current firstlevel subfolders
			if self.has_multi_root:
				folders = []
				for folder in self.project_abs_basepath:
					folders.append(self.valid_subfolders(folder))

			else: # no multiroot, no subroot
				# check if this the project is just a plain structure with just one single object inside (either HSF or GSM)
				basepath = self.project_abs_basepath[0]
				basename = os.path.basename(os.path.normpath(basepath))
				if is_dir(basepath, basename) or is_file(basepath, basename +'.gsm'):
					folders = self.project_abs_basepath  # return list
				else:
					folders = self.valid_subfolders(basepath)

		return folders

	def valid_subfolders(self, basepath):
		""" Returns a list of all subfolders, checked for being not empty by looking for HSF/GSM inside. """
		folders = [fldr for fldr in os.listdir(basepath) if (
			is_dir(basepath, fldr) and (
			is_dir(basepath, fldr, fldr) \
			or is_file(basepath, fldr, fldr +'.gsm')))]
		return folders

	def pick_working_dir(self, folders):
		""" Gets called if there are multiple folders in the project. 
		"""
		if self.has_multi_root:
			# list comprehension because multiroot has a nested structure
			# i.e. [[one, two], [three, four]]
			folderNames = [x for l in folders for x in l]
		else:
			folderNames = []
			for folder in folders:
				index = folder.rfind('/') + 1
				if index > 0:
					folderNames.append(folder[index:])
				else:
					folderNames.append(folder)

		# self.select will be called once with the indices (mapped from the folders)
		self.show_quick_panel(folderNames, self.select)

	def select(self, select):
		if self.has_multi_root:
			# now we have to resolve the problem of the flat `select` index
			# vs. the nested structure of a multi root
			folders = [x for l in self.folders for x in l]
		else:
			folders = self.folders
			
		if select < 0:  # will be -1 if panel was cancelled
			return
		self.working_dir = folders[select]
		self.delegator()  # go on here

	def show_quick_panel(self, options, done):
		""" Shows the Sublime Text quick panel with the invoked options. """
		# Sublime Text 3 requires a short timeout between quick panels
		sublime.set_timeout(lambda: self.window.show_quick_panel(options, done), 10)

	def normpath(self, path):
		""" Normalize a pathname by collapsing redundant separators.
			On Windows, it converts forward slashes to backward slashes.
			Returns the object as an quote encapsulated string (as needed for the CLI).
		"""
		return '"{}"'.format(os.path.normpath(path))

	def delegator(self):
		""" Delegates back to the specific calling class.
			Also makes the `working_dir` path absolut.
		"""
		try:
			if not self.on_post_save_state:
				if self.has_subroot:
					# join with new root
					self.working_dir = os.path.join(self.sub_root_path, self.working_dir)
				# make absolut path, since relative paths might introduce errors
				self.working_dir = os.path.join(self.project_abs_basepath[0], self.working_dir)
			else: # we are coming from the on_post_save event listener
				self.working_dir = os.path.join(*splitall(self.active_file_path)[:-2])
		except Exception as e:
			raise e
		
		log.debug("Working Dir: {}".format(self.working_dir))
		
		# this delegates back to the calling class.
		self.on_done_proj()


############################################################################	
class HsfBuildCommand(Builder):
	""" Converts a GSM into human readable GDL scripts via the LP_XMLConverter. """
	# go to
	# http://gdl.graphisoft.com/tips-and-tricks/how-to-use-the-lp_xmlconverter-tool
	# for detailed information

	def run(self, *args, **kwargs):
		""" Sublime Text will call this function.
			We will run the parent class "Builder" first.
			That will give us all the parameters we need.
		"""
		self.on_post_save_state = False
		super().run(self)

	def on_done_proj(self):
		# we're coming from super().delegator()
		# own function because quick panel is async
		self.find_gsm()

	def find_gsm(self):
		self.files = []
		log.debug(self.working_dir)
		# r=root, d=directories, f=files
		for r, d, f in os.walk(self.working_dir):
			for file in f:
				# casefolding because the user might have all caps extension
				# https://docs.python.org/3/library/stdtypes.html#str.casefold
				folded = str.casefold(file)
				if folded.endswith('.gsm'):
					self.files.append(os.path.join(r, file))

		if len(self.files) <= 0:
			err("GDL build error: No GSM found.")
		elif len(self.files) > 1:
			self.show_quick_panel(self.files, self.select_gsm)
		else:
			self.file_to_convert = self.files[0]
			self.on_done_file()  # go on here

	def on_done_file(self):
		self.cmdargs = get_project_data(self.view, 'to-hsf')
		self.run_hsf()

	def select_gsm(self, select):
		if select < 0:
			return
		self.file_to_convert = self.files[select]
		self.on_done_file()  # go on here
	
	def run_hsf(self, ):
		""" Invokes the LP_XML converter. 
		"""
		# normpath all to just be sure the CLI will take them without complain
		self.converter = super().normpath(self.converter)
		self.file_to_convert = super().normpath(self.file_to_convert)
		self.working_dir = super().normpath(self.working_dir)

		cmd = [self.converter, "libpart2hsf", self.cmdargs, self.file_to_convert, self.working_dir] # cmd, source, dest
		cmd = list(filter(None, cmd))  # filters out the empty cmdargs. otherwise Macs get hiccups. sigh.
		cmd = " ".join(cmd)

		#log.debug("GDL Command run: " + " ".join(cmd)) # gets logged automatically by ST
		execCMD = {"shell_cmd": cmd}
		
		self.window.run_command("exec", execCMD)

############################################################################
class LibpartBuildCommand(Builder):
	""" Builds a GSM from the GDL scripts in the project. """

	def run(self, *args, **kwargs):
		""" Sublime Text will call this function. """
		# if this function however is called from the on_post_save event listener
		# then we want to bypass the selection part
		self.active_file_path = sublime.active_window().active_view().file_name()
		if 'on_post_save_state' in kwargs:
			log.debug("This command is called on post save.")
			log.debug("Current active file is: {}".format(self.active_file_path))
			self.on_post_save_state = kwargs.get('on_post_save_state')
		else:
			self.on_post_save_state = False

		super().run(self)

	def on_done_proj(self):
		# we're coming from super().delegator()
		# own function because quick panel is async
		self.find_hsf()

	def find_hsf(self):
		""" Finds all possible folders for converting to GSM. 
		"""
		if self.on_post_save_state:
			self.folder_to_convert = self.working_dir
		else:
			if len(self.folders) <= 0:
				err("GDL build error: No HSF found.")

			# this assumes the user follows the scheme to have a subfolder of the same name
			last_part_of_path = os.path.basename(os.path.normpath(self.working_dir))

			self.folder_to_convert = os.path.join(self.working_dir, last_part_of_path)
		self.on_done_file()  # go on here

	def on_done_file(self):
		""" Path handling for GSM output.
		"""
		self.global_gsm_path = str(self.pckg_settings.get("global_gsm_path", ""))
		self.proj_gsm_path = get_project_data(self.view, 'proj_gsm_path')

		output_path = ""
		if self.proj_gsm_path:  # project based path takes precedence
			if self.proj_gsm_path != "default":
				# only set the path if its not 'default' which mimics the standard behavior
				# TODO implement path check here
				output_path = self.proj_gsm_path
		elif self.global_gsm_path:  # otherwise take global path, if set
			output_path = self.global_gsm_path

		if not output_path:
			# default path => not global or proj path is set, or proj path says 'default'
			output_path = os.path.dirname(self.folder_to_convert)

		gsm_name = os.path.basename(os.path.normpath(self.folder_to_convert)) + ".gsm"
		self.gsm_path = os.path.join(output_path, gsm_name)

		self.cmdargs = get_project_data(self.view, 'to-gsm')

		self.run_libpart()

	def run_libpart(self):
		""" Invokes the LP_XML converter. 
		"""
		self.converter = super().normpath(self.converter)
		self.folder_to_convert = super().normpath(self.folder_to_convert)
		self.gsm_path = super().normpath(self.gsm_path)

		cmd = [self.converter, "hsf2libpart", self.cmdargs, self.folder_to_convert, self.gsm_path] # cmd, source, dest
		cmd = list(filter(None, cmd))  # filters out the empty cmdargs. otherwise Macs get hiccups. sigh.
		# if you use `cmd` instead of `shell_cmd` you will get the infamous [Winerror 5]
		# see: https://forum.sublimetext.com/t/winerror-5-access-is-denied/
		# however, for `shell_cmd` to work we need to pass a string, not a list (!)
		cmd = " ".join(cmd)

		# log.debug("GDL Command run: " + cmd)
		execCMD = {"shell_cmd": cmd}

		self.window.run_command("exec", execCMD)

