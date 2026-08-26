import time
nitro = 0
valnerable  = False
boost = False
boost_time = 2
currentTime = 0
def nitro_add():
    global nitro
    nitro+=1
def after_detection():
    global nitro,valnerable,boost,boost_time
    if nitro > 0 and not boost:
        nitro -=1
        valnerable = False
        boost = True
        currentTime = time.time() + boost_time
def response():
    global valnerable,boost
        
