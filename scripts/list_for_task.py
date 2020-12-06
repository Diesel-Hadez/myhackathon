task_table=[]
def input_skill_task(task_table,skill,task):
    for i in range(len(task_table)):
        if task_table[i][0]==skill:
            task_table[i][1]+=task
            return task_table
    else:
        task_table.append([skill,task])
        return task_table


def search_task(skill):
    for i in range(len(task_table)):
        if task_table[i][0]==skill:
            return task_table[i][1]


