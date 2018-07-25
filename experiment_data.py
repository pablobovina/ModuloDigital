

class ExperimentData:

    def __init__(self, cpoints, repeat):
        self.repeat = repeat
        self.cpoints = cpoints

    def __iter__(self):
        return self

    def next(self):
        if self.repeat == 1:
            self.repeat -= 1
            return self.cpoints
        if self.repeat > 1:
            for cpoint in self.cpoints:
                ExperimentData._shift_phase_list(cpoint)
            self.repeat -= 1
            return self.cpoints
        if self.repeat <= 0:
            raise StopIteration()

    @staticmethod
    def _shift_phase_list(cpoint):
        phase_list = cpoint["phase"]
        cpoint["phase"] = phase_list[1:] + phase_list[:1]
        return cpoint
