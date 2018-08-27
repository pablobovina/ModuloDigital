import logging

logger = logging.getLogger("modDig")


class ExperimentData:

    def __init__(self, cpoints, repeat):

        errors = []
        self._check_cpoints(cpoints, errors)
        self._check_repeat(repeat, errors)

        if errors:
            for error in errors:
                logger.error(error)
            raise Exception("error create experiment data " + ";".join(errors))

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

    @staticmethod
    def _check_repeat(repeat, errors=None):
        if not (repeat > 0 and isinstance(repeat, int)):
            errors.append("repeat debe ser un numero entero mayor a 0")
        return

    @staticmethod
    def _check_cpoints(cpoints, errors=None):
        if not (cpoints and isinstance(cpoints, list)):
            errors.append("cpoints debe ser un una lista no vacia de instrucciones")
        return
