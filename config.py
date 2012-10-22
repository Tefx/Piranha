import sys; 
sys.path.append("/Users/zzm/Desktop/Corellia")
sys.path.append("/Users/zzm/Desktop/Husky")
sys.path.append("/Users/zzm/Desktop/Thinkpol")
sys.path.append("/Users/zzm/Desktop/Piranha")
sys.path.append("../")


redis_conf = {
    "host" : "localhost",
    "port" : 6379,
    "db" : 0
}

timeout = 5

queuepool_port = 9999
queuepool_host = "localhost"
queuepool_addr = queuepool_host, queuepool_port

web_port = 8080
web_server = "auto"

miniture_addr = ("localhost", 10000)

supervisor_port = 7890
