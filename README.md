# MarkdownToHtml

Sometimes I need to output my markdown file to html. However, I did not find a appropriate local editor to help me. It does have some excellent online markdown editors, and they also support html. But I am not used to write markdown in the website. So I tried to use python to write a simple software to help me, namely MarkdownToHtml. The MarkdownToHtml is based on PySide Module, which is quite powerful for me. Otherwise, I put all the codes in a single .py file since not much.

2018/02/17: still in progress. I will finish it in next two days.
2018/02/18: got trouble in Qt Delegate. Where the event pass through eventFilter method of QtGui.QStyledItemDelegate come from? I re-define the keyPreeEvent method of QtGui.TreeView and try to catch the event, but it not always work. Anyway, I skipped it.
