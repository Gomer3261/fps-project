class SESSIONS:
    class TICKETBOOTH:
        nextTicket = 1
        def getTicket(self):
            ticket = nextTicket
            self.nextTicket += 1
            return ticket
    TicketBooth = TICKETBOOTH()

    storage = {}
    
    def store(self, info):
        ticket = self.TicketBooth.getTicket()
        self.storage[ticket] = info
        return ticket

    def checkout(self, ticket):
        info = self.storage[ticket]
        self.storage.pop(ticket)
        return info
