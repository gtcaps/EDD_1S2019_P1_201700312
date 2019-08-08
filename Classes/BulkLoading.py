from Structures.DoubleCircularList import DoubleCircularList

class BulkLoading:

    def __new__(cls, file_name):
        file = open("{}.csv".format(file_name), "r")
        players_list = DoubleCircularList()
        first_line = False
        for player in file:
            if first_line is False:
                first_line = True
                continue
            players_list.add(player)
        file.close()

        return players_list




