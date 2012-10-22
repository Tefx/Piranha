1. project可以包含project或者task
2. project对应QueuePool
3. task对应Queue
4. 同一个Queue中任务没有优先级
5. 可以将Worker添加到某个位置
6. 将worker添加到某个位置包括register function和设置前缀


For Client:
1. PushTask("/A/B/task0", task)     PUT    
2. FetchResult("/A/B/key", key)      GET    
3. MkTask("/A/B/task0", function)    PUT    
4. RmTask("/A/B/task0")    DELETE    
5. MkProj("/A/B")    PUT    
6. RmProj("/A/B")    DELETE    
7. AddWorkers("/A/B/task", 10)     UPDATE   
8. RmWorkers("/A/B/task0", 10)    UPDATE


POST "/A/B/task"     提交任务     push_task
GET "/A/B/task/id"   获取结果     fetch_result

POST "/A/B"          创建任务     add_task
PUT "/A/B/task"      修改任务     add/delete_workers
DELETE "/A/B/task"   删除任务     delete

POST "/A"            创建项目     add_project
DELETE "/A/B"        删除项目     delete

add_worker:
remove_worker:

Project-Task

TaskQueue

push_task
pop_task
put_result
fetch_result

handler
waitting_queue
deleting_queue
running_queue
result_dict
path

Project

children [Project, Queue]
name

add_project
delete_project

add_task
delete_task

fetch_obj

push_task
pop_task
put_result
fetch_result