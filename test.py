from decoder import decodePayload

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

for d in range(200):
  start = time.time()
  decodePayload('MeteoHelix IoT',data[0])
  end = time.time()
  print(end - start)
