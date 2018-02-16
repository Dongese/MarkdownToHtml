from PySide import QtGui, QtCore,QtWebKit

class MarkdownEditor(QtGui.QWidget):
	def __init__(self):
		super(MarkdownEditor,self).__init__()
		self.setLayout(self._createEditor())
		self._settingEditor()

	def _createEditor(self):
		#Group box for editor and its label
		editorGroup = QtGui.QGroupBox()
		#create the layout
		layout = QtGui.QVBoxLayout()
		#create the model
		model = QtGui.QStringListModel()
		model.setStringList([""]*20)
		#create the editor
		self.editor = TableView()
		self.editor.setModel(model)
		#create the label for editor
		editorLabel = QtGui.QLabel("MARKDOWN")
		# add the label and editor to layout
		layout.addWidget(editorLabel)
		layout.addWidget(self.editor)
		#set layout to the editorGroup
		editorGroup.setLayout(layout)

		#Group box for preview
		previewGroup = QtGui.QGroupBox()
		#create the layout
		layout = QtGui.QVBoxLayout()
		#create the webView widget for preview
		webView = QtWebKit.QWebView()
		#create the label for the webView
		webViewLabel = QtGui.QLabel("PREVIEW")
		# set the label and preview to the layout
		layout.addWidget(webViewLabel)
		layout.addWidget(webView)
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
	    newItem = TextWidget()
	    self.editor.setItemDelegate(newItem)


class QTextEdit(QtGui.QTextEdit):
	def __init__(self,parent):
		super(QTextEdit,self).__init__(parent)


class TextWidget(QtGui.QStyledItemDelegate):
	def __init__(self):
		super(TextWidget,self).__init__()

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
			if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Down:
				event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress,QtCore.Qt.Key_Tab,QtCore.Qt.KeyboardModifier(),"",False,1)

			if event.key() == QtCore.Qt.Key_Backspace or event.key() == QtCore.Qt.Key_Left:
				if editor.textCursor().anchor() == 0:
					event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress,QtCore.Qt.Key_Backtab,QtCore.Qt.KeyboardModifier(),"",False,1)

			if event.key() == QtCore.Qt.Key_Up:
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
		self.setFixedSize(600,600)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    editor = MarkdownEditor()
    editor.show()
    sys.exit(app.exec_())    
