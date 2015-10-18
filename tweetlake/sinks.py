class Sink:
    '''
    Sink is data collection point.
    '''
    def __init__(self, *args, **kwargs):
        pass

    def write(self, data):
        raise NotImplementedError('This is a base class method. Implement this in your class.')

class FileSink(Sink):
    '''
    FileSink writes data in a file.
    '''

    def __init__(self, path):
        self.file = open(path, 'a')

    def write(self, data):
        self.file.write(data)

    def close(self):
        self.file.close()
