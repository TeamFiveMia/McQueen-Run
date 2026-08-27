import time
nitro = 0
vulnerable  = False
boost = False
boost_time = 2
currentTime = 0
def nitro_add():
    global nitro
    nitro+=1
def after_detection():
    global nitro,vulnerable,boost,boost_time
    if nitro > 0 and not boost:
        nitro -=1
        vulnerable = False
        boost = True
        endTime = time.time() + boost_time
def response():
    global vulnerable,boost
    if boost and time.time()>= endTime:
        boost = False
        vulnerable = True
        return "Nitro Done",True
    return "Nitro not Done",False
        
