import Pyro4


@Pyro4.expose
class StockMarket:
    def match_orders(self, order1, order2):
        print("hello")
        return 1


daemon = Pyro4.Daemon(port=12345)


uri = daemon.register(StockMarket, "stockmarket")

print("URI:", uri)

daemon.requestLoop()
