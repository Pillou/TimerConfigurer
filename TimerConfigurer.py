import sys
import json

class Range:
    def __init__(self, a, b):
        assert(a<b)
        self.a = a
        self.b = b
    def get(self):
        return [self.a, self.b]
    def get_max(self):
        return self.b
    def get_min(self):
        return self.a
    def contains(self, value):
        return (self.a <= value and value <= self.b)


class Timer :
    def __init__(self, clk_freq, prescaler_range, compare_range, wanted_freq):
        assert(clk_freq>wanted_freq)
        assert(prescaler_range.get_min() > 0)
        assert(compare_range.get_min() > 0)
        self.clk_freq = clk_freq
        self.prescaler_range = prescaler_range
        self.compare_range = compare_range
        self.wanted_freq = wanted_freq
        self.error = 0
        self.best_freq = 0
        self.compare = 0
        self.prescaler = 0

    def computeBestFreq(self):
        min_prescaler = int(self.wanted_freq * self.compare_range.get_max() / self.clk_freq)
        print("min_prescaler = {0}".format(min_prescaler))
        if(min_prescaler<self.prescaler_range.get_min()):
            print("ERROR: the prescaler range is not enough to meet the requirements")
            return
        current_prescaler = min_prescaler
        while( current_prescaler <= self.prescaler_range.get_max()):
            compare_value = max(int(round(self.clk_freq / (current_prescaler * self.wanted_freq))), 1)
            error = self.clk_freq/(current_prescaler*compare_value)-self.wanted_freq
            print("compare_value = {0}, error = {1}".format(compare_value, error))

            if( error == 0):
                break
            current_prescaler = current_prescaler * 2
        
        


if __name__ == "__main__":
    print("Starting TimerConfigurer...")
    print(sys.argv)
    with open('test.json') as data_file:    
        data = json.load(data_file)
    print(data)
    
    assert(data["clock"])
    assert(data["prescaler_range"])
    assert(data["compare_range"])
    assert(data["out_freq"])

    prescaler_range = Range(data["prescaler_range"][0], data["prescaler_range"][1])
    compare_range = Range(data["compare_range"][0], data["compare_range"][1])
    timer = Timer(data["clock"], prescaler_range, compare_range, data["out_freq"])
    timer.computeBestFreq()


    
