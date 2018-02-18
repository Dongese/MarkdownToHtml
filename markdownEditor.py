from PySide import QtGui, QtCore,QtWebKit
from syntax import syntaxDict
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
		infoLabel   = QtGui.QLabel("WORDS:100")
		# add the label and editor to layout
		layout.addWidget(editorLabel,0,0)
		layout.addWidget(self.editor,1,0)
		layout.addWidget(infoLabel,2,0)
		#set layout to the editorGroup
		editorGroup.setLayout(layout)

		#Group box for preview
		previewGroup = QtGui.QGroupBox()
		#create the layout
		layout = QtGui.QGridLayout()
		#create the webView widget for preview
		webView = QtWebKit.QWebView()
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
		layout.addWidget(webView,1,0,1,2)
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
			self.writeHtml(self.model.stringList())
			self.copyData = self.model.stringList()

	def writeHtml(self,stringList):
		for item in stringList:
			if item == "":continue


class SyntaxHandler(object):
	def __init__(self,string):
		self.string     = string.split(" ")
		self.flag       = False
		self.headTag    = None
		self.endTag     = None
		self.lastEndTag = None
		self.spaceCount = 0

	def syntaxType1(self):
		self.string = [self.syntax(strItem) for strItem in self.string]

	def syntax(self,item):
		if self.flag: return item

		if item in syntaxDict: 
			syntaxs = syntaxDict[item].split(",")

		elif item == " ":
			self.spaceCount += 1
			syntaxs = ["<pre><code>","</code></pre>"] if self.spaceCount == 4 else []

		else:
			syntaxs = ["<p>","</p>"]


		if len(syntaxs) == 2: 
			self.headTag,self.endTag = syntaxs
			self.flag                = True

		elif len(syntaxs) == 4:
			self.headTag







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
