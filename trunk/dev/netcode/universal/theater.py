### The Theater ###

class THEATER:




    class TICKETBOOTH:
        nextTicket = 1
        def getTicket(self):
            ticket = self.nextTicket
            self.nextTicket += 1
            return ticket




    class SEAT:
        LIFE = 1

        import time

        handler = None
        info = {}
        
        lastcontact = 0.0

        def __init__(self):
            self.contact()
        
        def contact(self):
            import time
            self.lastcontact = time.time()

        def terminateIfStale(self, timeout=10.0):
            import time
            dif = time.time() - self.lastcontact
            if dif > timeout:
                self.terminate()
                print "Stale seat terminated."
                return 1 # went stale
            return 0 # still fresh!

        def terminate(self):
            self.LIFE = 0
            if self.handler:
                self.handler.terminate()
            self.handler = None
            self.info = {}



    TicketBooth = TICKETBOOTH()
    seats = {}

    def hasSeat(self, ticket):
        if ticket in self.seats:
            return True
        else:
            return False

    def getSeat(self, ticket):
        if ticket in self.seats:
            seat = self.seats[ticket]
            return seat
        else:
            return None

    # Creates a new seat for a handler.
    def putHandlerInSeat(self, handler):
        newSeat = self.SEAT()
        newSeat.handler = handler
        ticket = self.TicketBooth.getTicket()
        self.seats[ticket] = seat
        return ticket

    # Synonym for putHanderInSeat
    def seatHandler(self, handler):
        newSeat = self.SEAT()
        newSeat.handler = handler
        ticket = self.TicketBooth.getTicket()
        self.seats[ticket] = newSeat
        return ticket

    # Returns a list of all handlers (seat.handler)
    def getAllHandlers(self):
        handlers = []
        for ticket in self.seats:
            seat = self.seats[ticket]
            
            handler = seat.handler
            if handler:
                handlers.append(handler)
        return handlers

    

    ###########################
    ### CLEANING OPERATIONS ###
    ###########################

    def terminateStaleHandlers(self):
        for ticket in self.seats:
            seat = self.seats[ticket]
            handler = seat.handler
            if seat.handler:
                handler.terminateIfStale()

    def terminateStaleSeats(self):
        for ticket in self.seats:
            seat = self.seats[ticket]
            if not seat.handler:
                seat.terminateIfStale()
    
    # Just removes any handlers that have been terminated (handler.LIFE == 0)
    def trashDeadHandlers(self):
        for ticket in self.seats:
            seat = self.seats[ticket]
            
            handler = seat.handler
            if seat.handler:
                if not seat.handler.LIFE:
                    seat.handler = None

    def trashDeadSeats(self):
        deadTickets = []
        for ticket in self.seats:
            seat = self.seats[ticket]
            if not seat.LIFE:
                deadTickets.append(ticket)
        for deadTicket in deadTickets:
            self.terminateSeat(deadTicket)

    def cleanUp(self):
        self.terminateStaleHandlers()
        self.terminateStaleSeats()
        self.trashDeadHandlers()
        self.trashDeadSeats()




    def terminateSeat(self, ticket):
        seat = self.seats[ticket]
        seat.terminate()
        self.seats.pop(ticket)

    def terminate(self):
        seatsToTerminate = []
        for ticket in self.seats:
            seatsToTerminate.append(ticket)

        for ticket in seatsToTerminate:
            self.terminateSeat(ticket)

    # Moves the handler from oldseat to newseat (by tickets)
    # and then terminates the oldseat.
    def reclaim(self, oldticket, newticket):
        if not newticket in self.seats:
            return 0 # Cannot reclaim
        oldseat = self.getSeat(oldticket)
        newseat = self.getSeat(newticket)
        
        newseat.handler = oldseat.handler
        oldseat.handler = None

        self.seats[oldticket].terminate()
        return 1 # Success
