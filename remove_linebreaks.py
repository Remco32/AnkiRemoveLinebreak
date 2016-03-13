# -*- coding: utf-8 -*-
#
# Based upon https://ankiweb.net/shared/info/892669336 , edited with permission
# To make copy/pasting from PDF files less cumbersome
# Edited version made by Remco32
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Version: 1.0, 2016/03/13

import os
from anki.hooks import addHook
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QIcon, QAction
from anki.hooks import wrap
from aqt.editor import Editor
from anki.utils import json
from BeautifulSoup import BeautifulSoup
from aqt import mw
from aqt.utils import showInfo
from aqt import browser

def removeLinebreaks(str):
	return test(str.replace('</div>', ' '))
	
def test(str):
	return str.replace('<div>', '')

def cleanLinebreaks(self):
	""" Utility function that removes linebreaks from the field of the note that is currently being edited. """
	self.saveNow();
	self.mw.checkpoint(_("Remove all linebreaks"))
	text = self.note.fields[self.currentField]
	self.note.fields[self.currentField] = removeLinebreaks(text)
	self.stealFocus = True;
	self.loadNote();

def setupButtons(self):
	""" Adds removeLinebreaks keyboard shortcut and button to the note editor. """
	icons_dir = os.path.join(mw.pm.addonFolder(), 'remove_linebreaks', 'icons')
	b = self._addButton("cleanButton", lambda s=self: cleanLinebreaks(self),
		    text=" ", tip="Remove linebreaks from the selected field  (Ctrl+Shift+q)", key="Ctrl+Shift+q")
	b.setIcon(QIcon(os.path.join(icons_dir, 'linebreak.png')))

def bulkReplace(self):
	""" Performs search-and-replace on selected notes """
	nids = self.selectedNotes()
	if not nids:
		return
	# Allow undo
	self.mw.checkpoint(_("Removes linebreaks on selected cards"))
	self.mw.progress.start()
	# Not sure if beginReset is required
	self.model.beginReset()
	changed = self.col.findReplace(nids, # Selected note IDs
		'&nbsp;', # from
		' ',  # to whitespace
		True, # treat as regular expression
		None, # all note fields
		True) # case insensitivity
	self.model.endReset()
	self.mw.progress.finish()
	# Display a progress meter
	showInfo(ngettext(
            "%(a)d of %(b)d note updated",
            "%(a)d of %(b)d notes updated", len(nids)) % {
                'a': changed,
                'b': len(nids),
            })

def addMenuItem(self):
	""" Adds hook to the Edit menu in the note browser """
	action = QAction("Removes linebreaks, currently selected notes", self)
	self.bulkReplace = bulkReplace
	self.connect(action, SIGNAL("triggered()"), lambda s=self: bulkReplace(self))
	self.form.menuEdit.addAction(action)
	
# Add-in hook; called by the AQT Browser object when it is ready for the add-on to modify the menus
addHook('browser.setupMenus', addMenuItem)

Editor.cleanLinebreaks = cleanLinebreaks
Editor.setupButtons = wrap(Editor.setupButtons, setupButtons)
