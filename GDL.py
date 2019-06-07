# -*- coding: utf-8 -*-

import os
import sublime
import sublime_plugin
import sys
import logging as log

PACKAGE_SETTINGS = "GDL.sublime-settings"
DEFAULT_AC_PATH = "C:/Program Files/GRAPHISOFT/ARCHICAD 23"

def check_system():
	""" Returns the file ending of executables depending on the
		operating system of the user.
	"""
	if sys.platform.startswith('darwin'): # OSX
		return "/Contents/MacOS/LP_XMLConverter.app/Contents/MacOS/LP_XMLConverter"
	elif sys.platform.startswith('win'):  # Windows
		return "/LP_XMLConverter.exe"
	else:
		sublime.error_message("GDL build error: Your OS is not supported.")
		return

def save_all_files():
	""" Saves all files open in sublime.
		Mimics the 'save on build' behavior of Sublime Text.
	"""
	for window in sublime.windows():
		for view in window.views():
			if view.file_name() and view.is_dirty():
				view.run_command("save")

def get_project_data(view, invoke):  # invoke is either 'to-hsf' or 'to-gsm'
	""" Gets the data of the .sublime-project file.
		Returns additional arguments for the commandline operation,
		if the user has set any.
	"""
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
		
# class AutocompleteCaps(sublime_plugin.EventListener):
# 	def on_query_completions(self, view, prefix, locations):
# 		return suggestions
		
# go to
# http://gdl.graphisoft.com/tips-and-tricks/how-to-use-the-lp_xmlconverter-tool
# for detailed information
class HsfBuildCommand(sublime_plugin.WindowCommand):

	def run(self, *args, **kwargs):
		self.os = check_system()
		self.view = self.window.active_view()
		if self.view.settings().get("auto_save", True):
			save_all_files()

		settings = sublime.load_settings(PACKAGE_SETTINGS)
		self.AC_path = str(settings.get("AC_path", DEFAULT_AC_PATH))

		folders = self.window.folders()
		if len(folders) <= 0:
			sublime.error_message("GDL build command error: You must have a project open.")
		else:
			if len(folders) == 1:
				self.multipleFolders = False
				self.project_folder = folders[0]
				self.on_done_proj()  # go on here
			else:
				self.multipleFolders = True
				self.pick_project_folder(folders)

	def on_done_proj(self):
		# this needs to be in its own function, because
		#  the sublime text quick panel works asynchronous
		self.find_gsm()

	def on_done_file(self):
		self.cmdargs = get_project_data(self.view, 'to-hsf')
		self.run_hsf()

	def pick_project_folder(self, folders):
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
		folders = self.window.folders()
		if select < 0:  # will be -1 if panel was cancelled
			return
		self.project_folder = folders[select]
		self.on_done_proj()  # go on here

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

	def select_gsm(self, select):
		if select < 0:
			return
		self.file_to_convert = self.files[select]
		self.on_done_file()  # go on here

	# Sublime Text 3 requires a short timeout between quick panels
	def show_quick_panel(self, options, done):
		sublime.set_timeout(lambda: self.window.show_quick_panel(options, done), 10)

	def run_hsf(self, ):
		converter = self.AC_path + self.os
		cmd = [converter, "libpart2hsf", self.cmdargs, self.file_to_convert, self.project_folder] # cmd, source, dest
		cmd = list(filter(None, cmd))  # filters out the empty cmdargs. otherwise Macs get hiccups. sigh.
		log.debug("GDL Command run: " + " ".join(cmd))
		execCMD = {"cmd": cmd}
		
		self.window.run_command("exec", execCMD)

############################################################################
class LibpartBuildCommand(sublime_plugin.WindowCommand):

	def run(self, *args, **kwargs):
		self.os = check_system()
		self.view = self.window.active_view()
		if self.view.settings().get("auto_save", True):
			save_all_files()

		settings = sublime.load_settings(PACKAGE_SETTINGS)
		self.AC_path = str(settings.get("AC_path", DEFAULT_AC_PATH))

		folders = self.window.folders()
		if len(folders) <= 0:
			sublime.error_message("GDL build command error: You must have a project open.")
		else:
			if len(folders) == 1:
				self.multipleFolders = False
				self.project_folder = folders[0]
				self.on_done_proj()  # go on here
			else:
				self.multipleFolders = True
				self.pick_project_folder(folders)

	def on_done_proj(self):
		# own function because quick panel is async
		self.find_hsf()

	def on_done_file(self):
		self.gsm_name = self.folder_to_convert + ".gsm"
		self.cmdargs = get_project_data(self.view, 'to-gsm')
		self.run_libpart()

	def pick_project_folder(self, folders):
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
		folders = self.window.folders()
		if select < 0:  # will be -1 if panel was cancelled
			return
		self.project_folder = folders[select]
		self.on_done_proj()  # go on here

	def find_hsf(self):
		# self.folders = []
		#for fldr in os.listdir(self.project_folder):
		# for  fldr in os.scandir(self.project_folder):
		# 	self.folders.append(fldr.name)
		self.folders = [fldr for fldr in os.listdir(self.project_folder) if os.path.isdir(os.path.join(self.project_folder, fldr))]
		print(self.folders)

		if len(self.folders) <= 0:
			sublime.error_message("GDL build error: No HSF found.")

		if len(self.folders) > 1:
			self.show_quick_panel(self.folders, self.select_hsf)
		else:
			self.folder_to_convert = self.project_folder + "\\" + self.folders[0]
			self.on_done_file()  # go on here

	def select_hsf(self, select):
		folders = self.folders
		if select < 0:  # will be -1 if panel was cancelled
			return
		self.folder_to_convert = self.project_folder + "\\" + folders[select]
		self.on_done_file()  # go on here

	# Sublime Text 3 requires a short timeout between quick panels
	def show_quick_panel(self, options, done):
		sublime.set_timeout(lambda: self.window.show_quick_panel(options, done), 10)

	def run_libpart(self):
		converter = self.AC_path + self.os
		cmd = [converter, "hsf2libpart", self.cmdargs, self.folder_to_convert, self.gsm_name] # cmd, source, dest
		cmd = list(filter(None, cmd))  # filters out the empty cmdargs. otherwise Macs get hiccups. sigh.
		log.debug("GDL Command run: " + " ".join(cmd))
		execCMD = {"cmd": cmd}

		self.window.run_command("exec", execCMD)
