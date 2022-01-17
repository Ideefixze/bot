from bot.MessageProcessor import *

def test_processors():
    class FirstLvlSubclass(MessageProcessor):
        @processor
        def proc1(self, message):
            message['proc1'] = message.get('proc1', 0) + 1

        @processor
        def proc2(self, message):
            message['proc2'] = message.get('proc2', 0) + 1
        
        def ignored1(self, message):
            message['ignored1'] = message.get('ignored1', 0) + 1
    
    class SecondLvlSubclass(FirstLvlSubclass):
        @processor
        def proc3(self, message):
            message['proc3'] = message.get('proc3', 0) + 1

        def ignored2(self, message):
            message['ignored2'] = message.get('ignored2', 0) + 1

        @processor
        def proc4(self, message):
            message['proc4'] = message.get('proc4', 0) + 1
    
    message = {}
    first = FirstLvlSubclass()
    second = SecondLvlSubclass()
    expected_results = {'proc1': 1, 'proc2': 1, 'proc3': 0, 'proc4': 0, 'ignored1': 0, 'ignored2': 0}

    first.process(message)
    print(message)
    for func, calls in expected_results.items():
        assert message.get(func, 0) == calls
        if 'proc' in func: expected_results[func] += 1
    
    second.process(message)
    for func, calls in expected_results.items():
        assert message.get(func, 0) == calls




