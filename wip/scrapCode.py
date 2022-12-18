def init_units(UNITS_NUM=18) -> List[Unit]:
    """Creates a list of unit pieces for the gameboard"""
    i,j,j1,j2,dd,best_dd,best = None
    h=960
    w=1280
    rad=34.64
    border_y = 108
    border_x = 115
    circle = Unit[UNITS_NUM]
    for unit in range(UNITS_NUM/2):
        circle[unit].num=unit
        circle[unit+UNITS_NUM/2].num=unit+UNITS_NUM/2
        def ti_restart():
            circle[unit].y= math.floor((random.randrange(0,4294967295)%960)-(34.64*2))+34.64
            circle[unit+UNITS_NUM/2].y=h-1-circle[unit].y
            j1 = circle[unit].y/(rad*2)
            j2 = circle[unit+UNITS_NUM/2].y/(rad*2)
            circle[unit].y+=border_y

            if not unit:
                circle[unit].x=rad
                if j1&1:
                    ti_restart()
            else:
                circle[unit].x=math.floor((random.randrange(0,4294967295)%((w-rad*2*2)/2))-(34.64*2))+34.64
        
        ti_restart()
        circle[unit+UNITS_NUM/2].x=w-1-circle[unit].x
        if j1&1:
            circle[unit].x+=rad
        if j2&1:
            circle[unit+UNITS_NUM/2].x+=rad
        circle[unit].x+=border_x
        circle[unit+UNITS_NUM/2].x+=border_x


# circle[unit][3]= math.floor((random.randrange(0,4294967295)%960)-(rad*2))+rad
