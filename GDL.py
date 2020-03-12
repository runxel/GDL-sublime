# -*- coding: utf-8 -*-

import os
import sublime
import sublime_plugin
import sys
import logging

log = logging.getLogger(__name__)

PACKAGE_SETTINGS = "GDL.sublime-settings"
DEFAULT_AC_PATH = "C:/Program Files/GRAPHISOFT/ARCHICAD 23"

def save_all_files():
	""" Saves all files open in Sublime.
		Mimics the 'save on build' behavior of Sublime Text.
	"""
	for window in sublime.windows():
		for view in window.views():
			if view.file_name() and view.is_dirty():
				view.run_command("save")

def get_project_data(view, invoke):
	""" Gets the data of the .sublime-project file.
		Returns additional arguments for the commandline operation,
		if the user has set any.
	"""
	# invoke options: 'to-hsf' / 'to-gsm' / 'proj_gsm_path'
	project_data = view.window().project_data()
	if not project_data:
		sublime.error_message("You must create a project first! (Project > Save Project As...)")
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
		sublime.error_message("Something went wrong.")
		return

def get_project_newroot(view):
	""" Gets the data of the .sublime-project file.
		Returns a relative path, if set.
		(Useful, if you have many subfolders.)
	"""
	try:
		project_data = view.window().project_data()
		new_root_setting = project_data.get('root')
	except:
		new_root_setting = ""
	
	return new_root_setting


# Future addition. Sadly not working as by now.		
# class AutocompleteCaps(sublime_plugin.EventListener):
# 	def on_query_completions(self, view, prefix, locations):
# 		return suggestions


class Builder(sublime_plugin.WindowCommand):

	def run(self, *args, **kwargs):
		self.lp_conv_path = self.check_system()
		self.pckg_settings = sublime.load_settings(PACKAGE_SETTINGS)
		self.AC_path = str(self.pckg_settings.get("AC_path", DEFAULT_AC_PATH))
		self.converter = os.path.join(self.AC_path, self.lp_conv_path)

		self.view = self.window.active_view()
		if self.view.settings().get("auto_save", True):
			save_all_files()

		self.nr_path = get_project_newroot(self.view)
		log.debug(self.nr_path)
		# see if there is a relative path set in the project settings
		if self.nr_path != "":
			nr_path_abs = os.path.join(self.window.folders()[0], self.nr_path)
			self.folders = [directory for directory in os.listdir(nr_path_abs) if os.path.isdir(os.path.join(nr_path_abs, directory))]
		else:
			self.folders = self.window.folders()

		if len(self.folders) <= 0:
			sublime.error_message("GDL build command error: You must have a project open.")
		else:
			if len(self.folders) == 1:
				self.multipleFolders = False
				self.project_folder = self.folders[0]
				self.on_done_proj()  # go on here
			else:
				self.multipleFolders = True
				self.pick_project_folder(self.folders)

	def check_system(self):
		""" Returns the path to the LP_XML converter.
		"""
		if sys.platform.startswith('darwin'): # OSX
			self.os_win = "false"
			return "Contents/MacOS/LP_XMLConverter.app/Contents/MacOS/LP_XMLConverter"
		elif sys.platform.startswith('win'):  # Windows
			self.os_win = "true"
			return "LP_XMLConverter.exe"
		else:
			sublime.error_message("GDL build error: Your OS is not supported.")
			return

	def normpath(self, path):
		return '"{}"'.format(os.path.normpath(path))

	def pick_project_folder(self, folders):
		""" Gets called if there are multiple folders in the project. 
		"""
		folderNames = []
		for folder in folders:
			index = folder.rfind('/') + 1
			if index > 0:
				folderNames.append(folder[index:])
			else:
				folderNames.append(folder)

		# self.sel_proj will be called once, with the index of the selected item
		self.show_quick_panel(folderNames, self.select_project)

	def select_project(self, select):
		#folders = self.window.folders()
		folders = self.folders
		if select < 0:  # will be -1 if panel was cancelled
			return
		self.project_folder = folders[select]
		self.on_done_proj()  # go on here

	def show_quick_panel(self, options, done):
		""" Shows the Sublime Text quick panel with the invoked options. """
		# Sublime Text 3 requires a short timeout between quick panels
		sublime.set_timeout(lambda: self.window.show_quick_panel(options, done), 10)


# 	@classmethod
# 	def is_enabled(self):
# 		return "/GDL/" in self.window.active_view().settings().get("syntax")

		
# go to
# http://gdl.graphisoft.com/tips-and-tricks/how-to-use-the-lp_xmlconverter-tool
# for detailed information
class HsfBuildCommand(Builder):
	""" Converts a GSM into human readable GDL scripts. """

	def run(self, *args, **kwargs):
		""" Sublime Text will call this function. """
		super().run(self)

	def on_done_proj(self):
		# own function because quick panel is async
		self.find_gsm()

	def find_gsm(self):
		self.files = []
		# r=root, d=directories, f=files
		for r, d, f in os.walk(self.project_folder):
			for file in f:
				if '.gsm' in file:
					self.files.append(os.path.join(r, file))

		if len(self.files) <= 0:
			sublime.error_message("GDL build error: No GSM found.")

		if len(self.files) > 1:
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
		self.converter = super().normpath(self.converter)
		self.file_to_convert = super().normpath(self.file_to_convert)
		self.project_folder = super().normpath(self.project_folder)

		cmd = [self.converter, "libpart2hsf", self.cmdargs, self.file_to_convert, self.project_folder] # cmd, source, dest
		cmd = list(filter(None, cmd))  # filters out the empty cmdargs. otherwise Macs get hiccups. sigh.
		cmd = " ".join(cmd)

		#log.debug("GDL Command run: " + " ".join(cmd))
		execCMD = {"shell_cmd": cmd}
		
		self.window.run_command("exec", execCMD)

############################################################################
class LibpartBuildCommand(Builder):
	""" Builds a GSM from the GDL scripts in the project. """

	def run(self, *args, **kwargs):
		""" Sublime Text will call this function. """
		super().run(self)

	def on_done_proj(self):
		# own function because quick panel is async
		self.find_hsf()

	def find_hsf(self):
		""" Finds all possible folders for converting to GSM. 
		"""
		#self.folders = [fldr for fldr in os.listdir(self.project_folder) if os.path.isdir(os.path.join(self.project_folder, fldr))]

		if len(self.folders) <= 0:
			sublime.error_message("GDL build error: No HSF found.")

		# if len(self.folders) > 1:
		# 	self.show_quick_panel(self.folders, self.select_hsf)
		# else:
		# 	self.folder_to_convert = os.path.join(self.project_folder,self.folders[0])
		# 	self.on_done_file()  # go on here

		self.folder_to_convert = self.project_folder
		self.on_done_file()  # go on here

	def select_hsf(self, select):
		""" Selects on of the possible of folders of the find_hsf() def. 
		"""
		folders = self.folders
		if select < 0:  # will be -1 if panel was cancelled
			return
		self.folder_to_convert = os.path.join(self.project_folder, folders[select])
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
		cmd = " ".join(cmd)
		# log.debug("GDL Command run: " + cmd)

		# if you use `cmd` instead of `shell_cmd` you will get the infamous [Winerror 5]
		# see: https://forum.sublimetext.com/t/winerror-5-access-is-denied/
		# however, for `shell_cmd` to work we need to pass a string, not a list (!)
		execCMD = {"shell_cmd": cmd}

		self.window.run_command("exec", execCMD)

