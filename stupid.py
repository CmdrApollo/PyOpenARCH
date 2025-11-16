def __str__(self):
        contentstringlist = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]
        visited = [[False,False,False,False],[False,False,False,False],[False,False,False,False],[False,False,False,False]]
        contentstring = ""
        editable = self.current_tile_obj
        while True:
            if visited[editable.getlocation()[0]][editable.getlocation()[1]] == False:
                if type(editable.getcontents()) == None:
                    contentstringlist[editable.getlocation()[0]][editable.getlocation()[1]].append("   ")
                elif editable == self.current_tile_obj:
                    contentstringlist[editable.getlocation()[0]][editable.getlocation()[1]].append("[@]")
                else:
                    contentstringlist[editable.getlocation()[0]][editable.getlocation()[1]].append("[ ]")
            visited[editable.getlocation()[0]][editable.getlocation()[1]] = True
            exitcheck = True
            for i in range(len(visited)):
                for j in range(len(visited[i])):
                    if visited[i][j] == False:
                        exitcheck = False
            if exitcheck:
                for i in range(len(contentstringlist)):
                    for j in range(len(contentstringlist[i])):
                        contentstring += contentstringlist[i][j][0]
                    contentstring += "\n"
                return contentstring
            match editable:
                case editable if editable.north != None and visited[editable.north.getlocation()[0]][editable.north.getlocation()[1]] == False:
                    editable = editable.north
                case editable if editable.south != None and visited[editable.south.getlocation()[0]][editable.south.getlocation()[1]] == False:
                    editable = editable.south
                case editable if editable.east != None and visited[editable.east.getlocation()[0]][editable.east.getlocation()[1]] == False:
                    editable = editable.east
                case editable if editable.west != None and visited[editable.west.getlocation()[0]][editable.west.getlocation()[1]] == False:
                    editable = editable.west