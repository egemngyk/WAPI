from wapi import Widget

widget = Widget(path="widget.json")
widget.start()

input("Press Enter to stop...\n")

widget.stop()