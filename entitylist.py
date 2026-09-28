from functools import reduce

class EntityList(list):

    def filter(self, filter_lambda):
        tmp = filter(filter_lambda, self)
        #tmp = list(tmp)
        return EntityList(tmp)

    def sort(self, sort_lambda):
        tmp = sorted(self, key=sort_lambda)
        return EntityList(tmp)

    def map(self, map_lambda):
        tmp = map(map_lambda, self)
        return EntityList(tmp)

    def reduce(self, reduce_lambda, initial):
        return reduce(reduce_lambda, self, initial)

