from decoder import decodePayload
import unittest

data = [
  { "device": "367EEF",
     "provider": "sigfox",
     "seqNumber": "2440",
     "time": 1538731834,
     "snr": 23.97,
     "data": "14b6b8e622262e8408000000" },
   { "device": "367EEF",
     "provider": "orange",
    "seqNumber": "0",
    "time": 1538731802,
    "snr": 5,
    "data": "11bba6ce02b6700500268000" },
  { "device": "367EEF",
    "provider": "sigfox",
    "seqNumber": "3024",
    "time": 1538731853,
    "snr": 9.8,
    "data": "14b6f8be2726306b0d800000"
  } 
]

import time

class decoder_benchmark(unittest.TestCase):
  
  def test_benchmark(self):
    '''Not a real test...'''
    results = []
    for d in range(500):
      start = time.time()
      decodePayload('MeteoHelix IoT',data[0])
      end = time.time()
      results.append(end - start)
    print(sum(results) / len(results))
    self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()