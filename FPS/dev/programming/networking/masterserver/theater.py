### The Theater ###

class THEATER:




    class TICKETBOOTH:
        nextTicket = 0
        def getTicket(self):
            ticket = self.nextTicket
            self.nextTicket += 1
            return ticket




    class SEAT:
        LIFE = 1

        handler = None
        info = {}
        
        lastTime = 0.0

        def __init__(self):
            self.setLastTime()
        
        def setLastTime(self):
            import time
            self.lastTime = time.time()

        def terminateIfStale(self, timeout=120.0):
            import time
            dif = time.time() - self.lastTime
            if dif > timeout:
                self.terminate()
                return 1
            return 0

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
        seat = self.seats[ticket]
        return seat

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

    # Just removes any handlers that have been terminated (handler.LIFE == 0)
    def cleanUpDeadHandlers(self):
        for ticket in self.seats:
            seat = self.seats[ticket]
            
            handler = seat.handler
            if seat.handler:
                if not seat.handler.LIFE:
                    seat.handler = None

    def cleanUpDeadSeats(self):
        deadTickets = []
        for ticket in self.seats:
            seat = self.seats[ticket]
            if not seat.LIFE:
                deadTickets.append(ticket)
        for deadTicket in deadTickets:
            self.terminate(deadTicket)

    def cleanUp(self):
        self.cleanUpDeadHandlers()
        self.cleanUpDeadSeats()

    def terminate(self, ticket):
        seat = self.seats[ticket]
        seat.terminate()
        self.seats.pop(ticket)

    def terminateAll(self, ticket):
        for ticket in self.seats:
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
