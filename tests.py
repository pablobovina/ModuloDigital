exp = {"cpoints":
    [
        {"type": "continue", "pattern": "1" * 16, "demora": 4000000, "freq": 100000, "phase": [0, 90, 180, 270]},
        {"type": "loop", "pattern_init": "0" * 16, "pattern_end": "0" * 16, "ntimes": 5,
         "freq_init": 150000, "phase_init": [0, 90, 180, 270],
         "freq_end": 150000, "phase_end": [0, 90, 180, 270], "demora": 0, "instructions":
             [
                 {"type": "continue", "pattern": "0" * 16, "demora": 4000000, "freq": 100000,
                  "phase": [0, 90, 180, 270]},
                 {"type": "continue", "pattern": "1" * 16, "demora": 4000000, "freq": 150000,
                  "phase": [0, 90, 180, 270]}
             ]
         },
        {"type": "continue", "pattern": "0" * 16, "demora": 4000000, "freq": 100000, "phase": [0, 90, 180, 270]},
        {"type": "loop", "pattern_init": "0" * 16, "pattern_end": "0" * 16, "ntimes": 5,
         "freq_init": 150000, "phase_init": [0, 90, 180, 270],
         "freq_end": 150000, "phase_end": [0, 90, 180, 270], "demora": 0, "instructions":
             [
                 {"type": "continue", "pattern": "0" * 16, "demora": 4000000, "freq": 100000,
                  "phase": [0, 90, 180, 270]},
                 {"type": "continue", "pattern": "1" * 16, "demora": 4000000, "freq": 150000,
                  "phase": [0, 90, 180, 270]}
             ]
         }
    ],
    "repeat": 0,
    "ad": {"ts": 1000, "bloq": 1, "channels": 3},
    "name": "experimento de pruebas",
    "date": "11:00:00T05/03/2018",
    "author": "pbovina"
}

d1 = {
    "cpoints": [
        {"lsb": "1" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "1" * 8, "time": "4000000",
         "phase": "0, 90, 180, 270", "freq": "100000", "data": "0", "id": 1523141654228L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "L", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "5", "id": 1523141655342L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "0" * 8, "time": "4000000",
         "phase": "0, 90, 180, 270", "freq": "100000", "data": "0", "id": 1523141655519L},

        {"lsb": "1" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "1" * 8, "time": "4000000",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "0", "id": 1523141655520L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "R", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "0", "id": 1523141655697L},

        {"lsb": "1" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "1" * 8, "time": "4000000",
         "phase": "0, 90, 180, 270", "freq": "100000", "data": "0", "id": 1523141657471L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "L", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "5", "id": 1523141657632L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "0" * 8, "time": "4000000",
         "phase": "0, 90, 180, 270", "freq": "100000", "data": "0", "id": 1523141673163L},

        {"lsb": "1" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "1" * 8, "time": "4000000",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "0", "id": 1523141673164L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "R", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "0", "id": 1523141673328L}
    ],
    "settings": {
        "a_times": "0",
        "a_name": "Experimento de pruebas",
        "a_description": "Este es un experimento de pruebas",
        "a_freq": "100",
        "a_msb": "10000001",
        "a_freq_unit": "mhz",
        "a_ts_unit": "us",
        "a_lsb": "10000001",
        "a_ts": "1000",
        "a_bloq": "1",
        "a_channel": "3",
    }
}

d2 = {
    "cpoints": [
        {"lsb": "1" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "1" * 8, "time": "4000000",
         "phase": "0, 90, 180, 270", "freq": "100000", "data": "0", "id": 1523141654228L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "L", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "1", "id": 1523141655342L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "L", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "1", "id": 1523141655342L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "L", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "1", "id": 1523141655342L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "L", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "5", "id": 1523141655342L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "0" * 8, "time": "4000000",
         "phase": "0, 90, 180, 270", "freq": "100000", "data": "0", "id": 1523141655519L},

        {"lsb": "1" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "1" * 8, "time": "4000000",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "0", "id": 1523141655520L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "R", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "0", "id": 1523141655697L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "R", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "0", "id": 1523141655697L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "R", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "0", "id": 1523141655697L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "R", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "0", "id": 1523141655697L},

        {"lsb": "1" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "1" * 8, "time": "4000000",
         "phase": "0, 90, 180, 270", "freq": "100000", "data": "0", "id": 1523141657471L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "L", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "5", "id": 1523141657632L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "0" * 8, "time": "4000000",
         "phase": "0, 90, 180, 270", "freq": "100000", "data": "0", "id": 1523141673163L},

        {"lsb": "1" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "C", "msb": "1" * 8, "time": "4000000",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "0", "id": 1523141673164L},

        {"lsb": "0" * 8, "freq_unit": "hz", "t_unit": "ns", "type": "R", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "150000", "data": "0", "id": 1523141673328L}
    ],
    "settings": {
        "a_times": "0",
        "a_name": "Experimento de pruebas",
        "a_description": "Este es un experimento de pruebas",
        "a_freq": "100",
        "a_msb": "10000001",
        "a_freq_unit": "mhz",
        "a_ts_unit": "us",
        "a_lsb": "10000001",
        "a_ts": "1000",
        "a_bloq": "1",
        "a_channel": "3",
    }
}

d3 = {
    "cpoints": [
        {"lsb": "1" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "1" * 8, "time": "4000",
         "phase": "0, 90, 180, 270", "freq": "20", "data": "0", "id": 1523141654228L},
        {"lsb": "1" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "1" * 8, "time": "4000",
         "phase": "0, 90, 180, 270", "freq": "40", "data": "0", "id": 1523141654229L},
        {"lsb": "1" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "1" * 8, "time": "4000",
         "phase": "0, 90, 180, 270", "freq": "20", "data": "0", "id": 1523141654230L},

    ],
    "settings": {
        "a_times": "0",
        "a_name": "Experimento de pruebas",
        "a_description": "Este es un experimento de pruebas",
        "a_freq": "100",
        "a_msb": "10000001",
        "a_freq_unit": "mhz",
        "a_ts_unit": "us",
        "a_lsb": "10000001",
        "a_ts": "1000",
        "a_bloq": "1",
        "a_channel": "3",
    }
}

d4 = {
    "cpoints": [
        {"lsb": "1" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "1" * 8, "time": "4000",
         "phase": "0, 90, 180, 270", "freq": "1", "data": "0", "id": 1523141654228L},
        {"lsb": "1" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "1" * 8, "time": "4000",
         "phase": "0, 90, 180, 270", "freq": "2", "data": "0", "id": 1523141654229L}
    ],
    "settings": {
        "a_times": "0",
        "a_name": "Experimento de pruebas",
        "a_description": "Este es un experimento de pruebas",
        "a_freq": "100",
        "a_msb": "10000001",
        "a_freq_unit": "mhz",
        "a_ts_unit": "us",
        "a_lsb": "10000001",
        "a_ts": "1000",
        "a_bloq": "1",
        "a_channel": "3",
    }
}

d5 = {
    "cpoints": [
        {"lsb": "1" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "1" * 8, "time": "2000",
         "phase": "0, 90, 180, 270", "freq": "1", "data": "0", "id": 1523141654228L},

        {"lsb": "0" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "L", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "1", "data": "5", "id": 1523141655342L},

        {"lsb": "0" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "0" * 8, "time": "2000",
         "phase": "0, 90, 180, 270", "freq": "1", "data": "0", "id": 1523141655519L},

        {"lsb": "1" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "1" * 8, "time": "2000",
         "phase": "0, 90, 180, 270", "freq": "2", "data": "0", "id": 1523141655520L},

        {"lsb": "0" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "R", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "2", "data": "0", "id": 1523141655697L},

        {"lsb": "1" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "1" * 8, "time": "2000",
         "phase": "0, 90, 180, 270", "freq": "1", "data": "0", "id": 1523141657471L},

        {"lsb": "0" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "L", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "2", "data": "5", "id": 1523141657632L},

        {"lsb": "0" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "0" * 8, "time": "2000",
         "phase": "0, 90, 180, 270", "freq": "1", "data": "0", "id": 1523141673163L},

        {"lsb": "1" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "1" * 8, "time": "2000",
         "phase": "0, 90, 180, 270", "freq": "2", "data": "0", "id": 1523141673164L},

        {"lsb": "0" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "R", "msb": "0" * 8, "time": "0",
         "phase": "0, 90, 180, 270", "freq": "2", "data": "0", "id": 1523141673328L}
    ],
    "settings": {
        "a_times": "0",
        "a_name": "Experimento de pruebas",
        "a_description": "Este es un experimento de pruebas",
        "a_freq": "100",
        "a_msb": "10000001",
        "a_freq_unit": "mhz",
        "a_ts_unit": "us",
        "a_lsb": "10000001",
        "a_ts": "1000",
        "a_bloq": "1",
        "a_channel": "3",
    }
}

d6 = {
    "cpoints": [
        {"lsb": "0" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "1"*8, "time": "10000",
         "phase": "0", "freq": "10", "data": "0", "id": 1523141654228L},
        {"lsb": "0" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "0"*8, "time": "500",
         "phase": "90", "freq": "10", "data": "0", "id": 1523141654229L},
        {"lsb": "0" * 8, "freq_unit": "mhz", "t_unit": "ms", "type": "C", "msb": "1"*8, "time": "500",
         "phase": "180", "freq": "10", "data": "0", "id": 1523141654230L},
    ],
    "settings": {
        "a_times": "3",
        "a_name": "Experimento de pruebas",
        "a_description": "Este es un experimento de pruebas",
        "a_freq": "100",
        "a_msb": "10000001",
        "a_freq_unit": "mhz",
        "a_ts_unit": "us",
        "a_lsb": "10000001",
        "a_ts": "1",
        "a_bloq": "1",
        "a_channel": "3",
        "a_phase": "0"
    }
}

