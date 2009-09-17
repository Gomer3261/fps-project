### Notifications ###
INIT = 1

class NOTIFIER:

    notifications = []
    
    active = 0
    show = 0
    
    currentText = ""

    displayTime = 0.0
    startTime = 0.0
    currentTime = 0.0

    import time

    def notify(self, note, time=0.0):
        self.notifications.append( (note, time) )

    def run(self):
        if not self.active:
            if self.notifications:
                # Get next notice
                notice = self.notifications[0]
                self.notifications.pop(0)

                # Set the text
                import textwrap
                self.currentText = textwrap.fill(notice[0], 34)

                # Set the display time
                self.displayTime = (float( len(notice[0]) ) * 0.05) + 0.5 # Dynamic Display Time (0.05 seconds per character)
                if notice[1]:
                    # If this notice has preset displayTime, then use it.
                    self.displayTime = notice[1]

                # Start the clock
                self.startTime = self.time.time()
                self.active = 1
                self.show = 1

        if self.active:
            # Figure out the current time
            self.currentTime = self.time.time() - self.startTime

            if self.currentTime > self.displayTime:
                # Then hide the notifier
                self.show = 0

            if self.currentTime > (self.displayTime + 0.25):
                # After a second (Giving the notifier's animation time to hide itself)
                # turn of active which means the notifier is ready to handle another notification.
                self.active = 0

Notifier = NOTIFIER()

def notify(note, time=0.0):
    global Notifier
    Notifier.notifications.append( (note, time) )
