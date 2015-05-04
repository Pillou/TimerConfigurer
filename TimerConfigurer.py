#  TimerConfigurer.py
#
#  Copyright 2015 Guillaume Le Cam
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
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

    def GetMinPrescaler(self):
        min_prescaler = ComputePrescaler(self.clk_freq, self.wanted_freq, self.compare_range.get_max() )
        min_prescaler = max(int(min_prescaler), self.prescaler_range.get_min())
        return min_prescaler

    def GetMaxPrescaler(self):
        max_prescaler = ComputePrescaler(self.clk_freq, self.wanted_freq, self.compare_range.get_min() )
        max_prescaler = min(int(max_prescaler+1), self.prescaler_range.get_max())
        return max_prescaler


    def computeBestFreq(self):
        print("min_prescaler = {0}, max_prescaler = {1}".format(self.GetMinPrescaler(), self.GetMaxPrescaler()))
        current_prescaler = self.GetMinPrescaler()
        while( current_prescaler <= self.GetMaxPrescaler()):
            compare_value = max(int(round(self.clk_freq / (current_prescaler * self.wanted_freq))), 1)
            error = self.clk_freq/(current_prescaler*compare_value)-self.wanted_freq
            print("compare_value = {0}, error = {1}".format(compare_value, error))

            if( error == 0):
                break
            current_prescaler = current_prescaler * 2



def ComputePrescaler(ref_clk, wanted_freq, compare_value):
    return (ref_clk / (wanted_freq * compare_value) )

def ComputeCompareValue(ref_clk, wanted_freq, prescaler):
    return (ref_clk / (wanted_freq * prescaler) )


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



