
# circle[unit][3]= math.floor((random.randrange(0,4294967295)%960)-(rad*2))+rad


# original method of initializing units found in TempleOS
def init_units_test(UNITS_NUM=18) -> List[Unit]:
    """Creates a list of unit pieces for the gameboard"""
    HALF_UNITS_NUM=int(UNITS_NUM/2)
    h=960
    w=1280
    rad=30 #34.64
    cols=18#int((w-8-rad)/(2*rad))&~1-1
    border_x =(w+rad-cols*2*rad)/2
    rows=14#int(h/(2*rad))&~1
    border_y = 108#(h-rows*2*rad)/2

    circle = [[0 for x in range(10)] for x in range(UNITS_NUM)]
    for unit in range(HALF_UNITS_NUM):
        ti_restart = True
        circle[unit][0]=unit
        circle[unit+HALF_UNITS_NUM][0]=unit+HALF_UNITS_NUM
        while ti_restart:
            ti_restart=False
            num = random.randint(0,4294967295)%h
            circle[unit][3]= num-(num%(rad*2))+rad
            circle[unit+HALF_UNITS_NUM][3]=h-1-circle[unit][3]
            j1 = int(circle[unit][3]/(rad*2))
            j2 = int(circle[unit+HALF_UNITS_NUM][3]/(rad*2))
            circle[unit][3]+=border_y
            
            if not unit:
                circle[unit][2]=rad
                if j1&1:
                    ti_restart=True
            else:
                num = random.randint(0,4294967295)%(w-rad*2*2)/2
                circle[unit][2]= num-num%(rad*2)#math.floor((random.randrange(0,4294967295)%((w-rad*2*2)/2))-(rad*2))+rad
        circle[unit+HALF_UNITS_NUM][2]=w-1-int(circle[unit][2])

        if j1&1:
            circle[unit][2]+=rad
        if j2&1:
            circle[unit+HALF_UNITS_NUM][2]+=rad
        circle[unit][2]+=border_x
        circle[unit+HALF_UNITS_NUM][2]-=border_x

        def S2Circle(x,y):
            
            tempY=int((y-border_y)/(rad*2))
            if tempY&1:
                tempX=(x-rad-border_x)/(rad*2)
            else:
                tempX=(x-border_x)/(rad*2)
            return tempX,tempY

        def Circle2S(x,y):
            
            print(x,y)
            tempY=y*rad*2+rad+border_y
            tempX=x*rad*2+rad+border_x
            if int(tempY)&1:
                tempX+=rad
            return tempX,tempY

        circle[unit][2],circle[unit][3]=S2Circle(circle[unit][2],circle[unit][3])
        circle[unit][2],circle[unit][3]=Circle2S(circle[unit][2],circle[unit][3])

        circle[unit+HALF_UNITS_NUM][2],circle[unit+HALF_UNITS_NUM][3]=S2Circle(circle[unit+HALF_UNITS_NUM][2],circle[unit+HALF_UNITS_NUM][3])
        circle[unit+HALF_UNITS_NUM][2],circle[unit+HALF_UNITS_NUM][3]=Circle2S(circle[unit+HALF_UNITS_NUM][2],circle[unit+HALF_UNITS_NUM][3])

        circle[unit][4]=0
        circle[unit+HALF_UNITS_NUM][4]=1

        circle[unit][7]=True
        circle[unit+HALF_UNITS_NUM][7]=True

        if not unit:
            circle[unit][6]=LIGHT_CYAN
            circle[unit+HALF_UNITS_NUM][6]=LIGHT_MAGENTA
            circle[unit][9]=True
            circle[unit+HALF_UNITS_NUM][9]=True
        else:
            circle[unit][6]=DARK_CYAN
            circle[unit+HALF_UNITS_NUM][6]=DARK_MAGENTA
            circle[unit][9]=False
            circle[unit+HALF_UNITS_NUM][9]=False

    for unit in range(HALF_UNITS_NUM):
        if circle[unit][9]==True:
            circle[unit][5]=unit
            circle[unit+HALF_UNITS_NUM][5]=unit+HALF_UNITS_NUM
        else:
            best_dd=sys.maxsize
            for piece in range(HALF_UNITS_NUM):
                if circle[unit][0]!=circle[piece][0]:
                    dd=pow(circle[unit][2]-circle[piece][2], 2)+pow(circle[unit][3]-circle[piece][3], 2)
                    if circle[piece][2]<circle[unit][2] or circle[piece][9] and dd<best_dd:
                        best_dd=dd
                        best=piece
            circle[unit][5]=best
            circle[unit+HALF_UNITS_NUM][5]=best+HALF_UNITS_NUM
    num_alive=[HALF_UNITS_NUM]*2
    new_circle = create_circle(circle[0])
    print(new_circle)
    result = [new_circle]

    for unit in range(1,UNITS_NUM):
        new_circle = create_circle(circle[unit])
        print(new_circle)
        result.append(new_circle)
    
    return result

def create_circle(circle:list) -> Unit:
    return Unit(circle[0],(circle[2],circle[3]),circle[2],circle[3],circle[4],circle[5],circle[6],circle[7], 30.0,circle[9])

        
