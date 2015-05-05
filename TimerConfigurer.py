import sys
import json

# TODO : Add comments

DEFAULT_EXAMPLE_FILE = "example.json"
DEFAULT_OUT_FILE = "result.txt"

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
        self.result_error = -1
        self.result_freq = 0
        self.result_compare = 0
        self.result_prescaler = 0

    def __str__(self):
        out = "Reference clock = {0} Hz\n".format(self.clk_freq)
        out += "Prescaler range is {0} to {1}\n".format(self.prescaler_range.get_min(),\
                                                        self.prescaler_range.get_max())
        out += "Compare register range is {0} to {1}\n".format(self.compare_range.get_min(),\
                                                               self.compare_range.get_max())
        out += "Target frequency is {0} Hz\n\n".format(self.wanted_freq)
        if(self.result_error == -1):
            out += "No solution found with the current values!\n"
        else :
            out += "The best solution found is :\n"
            out += "error = {0} Hz\n".format(self.result_error)
            out += "out frequency = {0} Hz\n".format(self.result_freq)
            out += "compare register = {0}\n".format(self.result_compare)
            out += "prescaler = {0}\n".format(self.result_prescaler)
        return out
    
    def SaveToFile(self, file_name):
        f = open(file_name, "w")
        f.write(self.__str__())
        f.close

    def computeBestFreq(self):
        min_prescaler = int(self.wanted_freq * self.compare_range.get_max() / self.clk_freq)
        if(min_prescaler<self.prescaler_range.get_min()):
            print("ERROR: the prescaler range is not enough to meet the requirements")
            return
        current_prescaler = min_prescaler
        while( current_prescaler <= self.prescaler_range.get_max()):
            compare_value = max(int(round(self.clk_freq / (current_prescaler * self.wanted_freq))), 1)
            result_freq = self.clk_freq/(current_prescaler*compare_value)
            error = abs(result_freq - self.wanted_freq)
            if(self.result_error == -1 or error < self.result_error):
                self.result_error = error
                self.result_freq = result_freq
                self.result_compare = compare_value
                self.result_prescaler = current_prescaler

            if( error == 0):
                break
            current_prescaler = current_prescaler * 2


def PrintHelp():
    help_string = "TimerConfigurer is a script used to find the best couple \n"
    help_string+= "compare value/prescaler value of a timer.\n"
    help_string+= "This script was implemented and tested with Python 2.7.\n"
    help_string+= "Usage : TimerConfigurer <command> [<args>]\n"
    help_string+= "  --help       : print help\n"
    help_string+= "  -c           : create an example json file named example.json\n"
    help_string+= "  -i file_name : file_name is a json file containing the problem constraints\n\n"
    help_string+= "Example : TimerConfigurer.py -i test.json -o result.txt\n"
    help_string+= "          This will read the file test.json and print the result in result.txt\n"
    print(help_string)
    
def PrintDefaultFile(file_name):
    file_str = """
    {
        "clock": 48000000,
        "prescaler_range": [1, 128],
        "compare_range": [1, 65535],
        "out_freq": 14250
    }

    """
    f = open(file_name, "w")
    f.write(file_str)
    f.close()

if __name__ == "__main__":
    print("Starting TimerConfigurer...")
    
    if(len(sys.argv) < 2):
        PrintHelp()
    else :
        in_file = ""
        i = 1
        while(i<len(sys.argv)):
            if(sys.argv[i] == "--help"):
                PrintHelp()
            elif(sys.argv[i] == "-c"):
                PrintDefaultFile(DEFAULT_EXAMPLE_FILE)
            elif(sys.argv[i] == "-i"):
                i += 1
                in_file = sys.argv[i]

                with open(in_file) as data_file:
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

                timer.SaveToFile(DEFAULT_OUT_FILE)
                print(timer)
            else:
                print("Command : {0} not valid!\n".format(sys.argv[i]))
            i +=1



