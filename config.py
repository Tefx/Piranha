import sys; sys.path.append("/Users/zzm/Desktop/Corellia")

redis_conf = {
    "host" : "localhost",
    "port" : 6379,
    "db" : 0
}

timeout = 5

queuesconfig = { 
    "echo"  :   (redis_conf, timeout),
    "math"  :   (redis_conf, timeout)
}

queuepool_port = 9999
queuepool_host = "localhost"

web_port = 8080
web_server = "auto"

