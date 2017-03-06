import multiprocessing


class MultiProcessor(object):

    DEFAULT_PROCESSORS = multiprocessing.cpu_count() * 2

    def __init__(self, func, controller):
        self.func = func
        self.controller = controller

    def pool_map_async_result(self, processors=DEFAULT_PROCESSORS):
        pool = multiprocessing.Pool(processes=processors)
        result = pool.map_async(self.func, self.controller)
        pool.close()
        pool.join()
        return result.get()

if __name__ == '__main__':
    def function(a):
        print 'test {}'.format(a)
        return a * 2

    controller = range(8)
    x = MultiProcessor(function, controller=controller)
    result = x.pool_map_async_result(processors=32)
    print result

