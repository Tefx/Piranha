import sys; sys.path.append("/Users/zzm/Desktop/Corellia")

redis_conf = {
    "host" : "localhost",
    "port" : 6379,
    "db" : 0
}

queuesconfig = { 
    "echo"  :   (redis_conf, 5)
}

queuepool_port = 9999
queuepool_host = "localhost"

web_port = 8080
web_server = "auto"

