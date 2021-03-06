#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from PySide import QtGui, QtCore,QtWebKit
from syntax import syntaxDict,innerSyntax
import os 

class MarkdownEditor(QtGui.QWidget):
	def __init__(self):
		super(MarkdownEditor,self).__init__()
		self.setLayout(self._createEditor())
		self._settingEditor()
		self.copyData = []
		
	def _createEditor(self):
		#Group box for editor and its label
		editorGroup = QtGui.QGroupBox()
		#create the layout
		layout = QtGui.QGridLayout()
		#create the model
		self.model = QtGui.QStringListModel()
		self.model.setStringList([""]*20)
		#create the editor
		self.editor = TableView()
		self.editor.setModel(self.model)
		#create the label for editor
		editorLabel = QtGui.QLabel("MARKDOWN")
		self.infoLabel   = QtGui.QLabel()
		# add the label and editor to layout
		layout.addWidget(editorLabel,0,0)
		layout.addWidget(self.editor,1,0)
		layout.addWidget(self.infoLabel,2,0)
		#set layout to the editorGroup
		editorGroup.setLayout(layout)

		#Group box for preview
		previewGroup = QtGui.QGroupBox()
		#create the layout
		layout = QtGui.QGridLayout()
		#create the webView widget for preview
		self.webView = QtWebKit.QWebView()
		#create the label, the button for the webView
		webViewLabel = QtGui.QLabel("PREVIEW")
		button       = QtGui.QToolButton()
		button.setIcon(QtGui.QIcon(QtGui.QPixmap("icon.png").scaled(50,50,aspectMode=QtCore.Qt.KeepAspectRatio)))
		#button.setFlat(True)
		self.webSaveLabel = QtGui.QLabel("Autosave in %s" % os.getcwd())
		self.webSaveLabel.setAlignment(QtCore.Qt.AlignHCenter)
		# set the label, button and preview to the layout
		layout.addWidget(webViewLabel,0,0)
		layout.addWidget(button,0,1)
		layout.addWidget(self.webView,1,0,1,2)
		layout.addWidget(self.webSaveLabel,2,0,1,2)
		#set layout to the previewGroup
		previewGroup.setLayout(layout)

		# we need a horizontal layout to contain both editorGroup and previewGroup
		group = QtGui.QHBoxLayout()
		group.addWidget(editorGroup)
		group.addWidget(previewGroup)
		return group

	def _settingEditor(self):
	    #self.editor.palette().brush(QtGui.QPalette.Background).setStyle(QtCore.Qt.NoBrush)
	    #self.editor.setTextElideMode(QtCore.Qt.ElideNone)
	    self.editor.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
	    newItem = TextWidget(self)
	    self.editor.setItemDelegate(newItem)
	    
	def detectRefresh(self):
		if self.copyData != self.model.stringList():
			#self.infoLabel.setText("WORDS:%d" % sum([len(item.split(" ")) for item in self.model.stringList()]))
			self.writeHtml(self.model.stringList())
			self.webView.load(QtCore.QUrl.fromLocalFile(os.path.join(os.getcwd(),"save.html")))
			self.copyData = self.model.stringList()

	def writeHtml(self,stringList):
		with open("save.html","wt") as f:
			for item in stringList:
				if item == "":continue
				value = SyntaxHandler(item)
				f.write(value.syntaxHanler().encode('utf-8'))
				f.write("\n")

class SyntaxHandler(object):
	def __init__(self,string):
		self.string     = string.split("\n")
		
		self.upSyntax        = None
		self.downSyntax      = None
		self.innerUpSyntax   = None
		self.innerDownSyntax = None
		self.endSyntax       = []
		self.spaceRecord     = []
		
	def syntaxHanler(self):
		self.string = [self.syntax(stringLine) for stringLine in self.string]
		self.string = [stringLine for stringLine in self.string if stringLine is not None]
		self.endSyntax.reverse()
		self.string = " ".join(self.string + self.endSyntax)
		return self.string

	def syntax(self,stringLine):
		if stringLine.count(" ") == len(stringLine):return None
		stringLine = stringLine.split(" ")
		spaceCount = 0
		extraSpace = 1
		if self.upSyntax is None and self.downSyntax is None:
			for i in xrange(len(stringLine)):
				if self.upSyntax is not None and self.downSyntax is not None: break
				if stringLine[i].endswith("."):stringLine[i] = "."
				if stringLine[i] in syntaxDict:
					self.upSyntax,self.downSyntax = syntaxDict[stringLine[i]].split(",")
					if stringLine[i] in innerSyntax:
						self.innerUpSyntax, self.innerDownSyntax = innerSyntax[stringLine[i]].split(",")
					stringLine[i] = ""

				elif stringLine[i] == "":
					spaceCount += 1
					self.upSyntax,self.downSyntax = ("<pre><code>","</code></pre>") if spaceCount == 4 else (None,None)

				else:
					self.upSyntax, self.downSyntax = "<p>","</p>"
					extraSpace = 0

			self.spaceRecord.append(spaceCount)
			self.endSyntax.append(self.downSyntax)

			if self.innerUpSyntax is not None and self.innerDownSyntax is not None:
				self.endSyntax.append(self.innerDownSyntax)
				return " ".join([self.upSyntax] + [self.innerUpSyntax] + stringLine[spaceCount+extraSpace:])
			else:
				return " ".join([self.upSyntax] + stringLine[spaceCount+extraSpace:])
		else:
			for i in xrange(len(stringLine)):
				if stringLine[i] == "": spaceCount += 1
				if stringLine[i].endswith("."):stringLine[i] = "."
				if stringLine[i] in innerSyntax:
					self.spaceRecord.append(spaceCount)
					stringLine[i] = ""
					if spaceCount <= self.spaceRecord[-2]:
						return " ".join([self.innerDownSyntax] + [self.innerUpSyntax] + stringLine[spaceCount+extraSpace:])
					else:
						self.endSyntax.append(self.downSyntax)
						self.endSyntax.append(self.innerDownSyntax)
						return " ".join([self.upSyntax] + [self.innerUpSyntax] + stringLine[spaceCount+extraSpace:])


class QTextEdit(QtGui.QTextEdit):
	def __init__(self,parent):
		super(QTextEdit,self).__init__(parent)



class TextWidget(QtGui.QStyledItemDelegate):
	def __init__(self,widget):
		super(TextWidget,self).__init__()
		self.widget = widget

	def createEditor(self,parent,option,index):
		editor = QTextEdit(parent)
		editor.setAcceptRichText(False)
		editor.setHorizontalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff)
		editor.setVerticalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff)
		editor.setLineWrapMode(QtGui.QTextEdit.NoWrap)
		return editor

	def setEditorData(self,editor,index):
		value = index.model().data(index,QtCore.Qt.EditRole)
		editor.setText(value)
		for i in xrange(len(value)):editor.moveCursor(QtGui.QTextCursor.Right,QtGui.QTextCursor.MoveAnchor)

	def setModelData(self,editor,model,index):
		value = editor.toPlainText()
		model.setData(index,value,QtCore.Qt.EditRole)
		if index.row() == model.rowCount() - 1:
			model.insertRow(model.rowCount())
			index = model.index(model.rowCount()-1,0)
			model.setData(index,"")

	def eventFilter(self,editor,event):
		if event.type() == QtCore.QEvent.Type.KeyPress:

			self.widget.detectRefresh()

			if event.key() == QtCore.Qt.Key_Return:
				self.widget.editor.setRowHeight(self.widget.editor.currentIndex().row(),editor.document().size().height() + 20)

			if  event.key() == QtCore.Qt.Key_Down:
				if editor.textCursor().block() == editor.document().lastBlock():
					event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress,QtCore.Qt.Key_Tab,QtCore.Qt.KeyboardModifier(),"",False,1)

			if event.key() == QtCore.Qt.Key_Up:
				if editor.textCursor().block() == editor.document().firstBlock() and self.widget.editor.currentIndex().row() != 0:
					event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress,QtCore.Qt.Key_Backtab,QtCore.Qt.KeyboardModifier(),"",False,1)

		return super(TextWidget,self).eventFilter(editor,event)


class TableView(QtGui.QTableView):
	def __init__(self):
		super(TableView,self).__init__()
		self.setShowGrid(False)
		self.horizontalHeader().hide()
		self.horizontalHeader().setStretchLastSection(True)
		#self.setStyleSheet("selection-background-color:rgb(237,244,247);selection-color:black;")
		self.setColumnWidth(0,600)
		self.setMinimumSize(600,600)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    editor = MarkdownEditor()
    editor.show()
    sys.exit(app.exec_())    
