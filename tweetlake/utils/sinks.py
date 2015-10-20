import json

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

    def __init__(self, path, processor):
        self.file = open(path, 'a')
        self.processor = processor

    def write(self, data):
        self.file.write(json.dumps(self.processor.process(data)) + '\n')

    def delete(self, data):
        self.file.write(json.dumps(self.processor.process_delete(data)) + '\n')

    def close(self):
        self.file.close()
