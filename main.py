from WAPI import Widget

app = Widget(path="widget.json")

app.start()

input(">>")

app.stop()