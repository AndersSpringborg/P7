class Wine:
    def __init__(self, name, region, year, producer, type, critics_score="default", volume="default",  price="default", lwin=0):
        self.name = name
        self.price = price
        self.region = region
        self.year = year
        self.critics_score = critics_score
        self.producer = producer
        self.type = type
        self.volume = volume
        self.linkedWineLwin = lwin
