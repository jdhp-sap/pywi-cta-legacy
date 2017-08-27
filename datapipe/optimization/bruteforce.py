#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# This script is provided under the terms and conditions of the MIT license:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__all__ = []

import json
from scipy import optimize
from datapipe.optimization.objectivefunc.wavelets_mrfilter_delta_psi_sigma_scipy import ObjectiveFunction

def main():

    # PARSE OPTIONS ###########################################################

    func = ObjectiveFunction(input_files=["/Volumes/ramdisk/flashcam/fits/gamma/"])

    s1_slice = slice(1, 5, 1)
    s2_slice = slice(1, 5, 1)
    s3_slice = slice(1, 5, 1)
    s4_slice = slice(1, 5, 1)

    search_ranges = (s1_slice,
                     s2_slice,
                     s3_slice,
                     s4_slice)

    res = optimize.brute(func,
                         search_ranges,
                         full_output=True,
                         finish=None)     #optimize.fmin)

    print("x* =", res[0])
    print("f(x*) =", res[1])

    # SAVE RESULTS ############################################################

    res_dict = {
                "best_solution": res[0].tolist(),
                "best_score": float(res[1]),
                "solutions": res[2].tolist(),
                "scores": res[3].tolist()
               }

    with open("optimize_sigma.json", "w") as fd:
        json.dump(res_dict, fd, sort_keys=True, indent=4)  # pretty print format


if __name__ == "__main__":
    main()

