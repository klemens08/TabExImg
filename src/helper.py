import sys, os

class Helper:

    @staticmethod
    def print(message):
        Helper.enablePrint()
        print(message)
        Helper.blockPrint()

    @staticmethod
    def blockPrint():
        sys.stdout = open(os.devnull, 'w')

    @staticmethod
    def enablePrint():
        sys.stdout = sys.__stdout__
