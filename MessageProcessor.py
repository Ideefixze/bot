class MessageProcessor:
    message_processors = {}
    
    def process(self, message):
        for cls in reversed(type(self).__mro__):
            if issubclass(cls, MessageProcessor) and cls is not MessageProcessor:
                for p in cls.message_processors[cls.__name__]:
                    p(self, message)

def processor(func):
    cls = func.__qualname__.split('.')[-2]
    if not cls in MessageProcessor.message_processors:
        MessageProcessor.message_processors[cls] = []
    MessageProcessor.message_processors[cls].append(func)
    return func
