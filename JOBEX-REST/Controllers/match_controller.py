from enum import Enum

class MatchController:

    object_types = Enum(STUDENT = 1,HRMANAGER = 2,MATCH = 3,POSITION=4)

    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if MatchController.__instance == None:
            MatchController()
        return MatchController.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MatchController.__instance != None:
            self.__instance
        else:
            MatchController.__instance = self

    def rematch(self, object_id, object):

        if object == self.object_types.STUDENT:
            return 1
        if object == self.object_types.POSITION:
            return 4

        return None
