from OpenSoar.utilities.helper_functions import seconds_time_difference


class Trip:

    def __init__(self, task, trace):

        task_result = task.apply_rules(trace)

        self.fixes = task_result[0]
        self.refined_start_time = task_result[1]
        self.outlanding_fix = task_result[2]
        self.distances = task_result[3]
        self.finish_time = task_result[4]

    def completed_legs(self):
        return len(self.fixes) - 1

    def outlanding_leg(self):
        if self.outlanded():
            return len(self.fixes) - 1
        else:
            return None

    def outlanded(self):
        return self.outlanding_fix is not None

    def fix_on_leg(self, fix, leg):
        """
        Return whether fix takes place within certain leg, excluding the boundaries
        :param fix: 
        :param leg: 
        :return: 
        """
        if leg + 1 > self.completed_legs():
            raise ValueError('Leg is not completed')
        else:
            larger_than_minimum = seconds_time_difference(self.fixes[leg]['time'], fix['time']) >= 0
            smaller_than_maximum = seconds_time_difference(fix['time'], self.fixes[leg + 1]['time']) >= 0
            return larger_than_minimum and smaller_than_maximum
