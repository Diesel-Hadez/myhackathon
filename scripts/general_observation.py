##This aims to return
##skill needed for specific job
##skill needed for specific job of specific level
"""
##Example dataset---uncomment this to try

jobs_lst=['job1',
          'job2',
          'job3']

general_skill_for_job=[['a','b','c'],
                       ['d','e','f'],
                       ['g','h','i']]

jobs_levels=[['junior','senior job 1'],
             ['associate job 2'],
             ['intern job 3','manager job3']]

skills_for_levels_jobs=[[['medium communication skill','good problem solving skill'],['skill_seniorjob2']],
                        [['skill_associatejob2']],
                        [['skill_internjob3'],['skill_managerjob3']]]
"""



def general_skill(job,jobs_lst,general_skill_for_job):
    print("General skill for ",job,"is :")
    for i in range(len(jobs_lst)):
        if jobs_lst[i]==job:
            for j in range(len(general_skill_for_job[i])):
                print (general_skill_for_job[i][j])



def skill_for_different_level(job,level,jobs_lst,jobs_levels,skills_for_levels_jobs):
    index_job=0
    index_level=0
    print("Skills required for",level,"level of",job,"are:")
    for i in range(len(jobs_lst)):
        if jobs_lst[i]==job:
            index_job=i
    for j in range(len(jobs_levels[index_job])):
        if jobs_levels[index_job][j]==level:
            index_level=j
    for k in range(len(skills_for_levels_jobs[index_job][index_level])):
        print(skills_for_levels_jobs[index_job][index_level][k])



"""
can try out for

general_skill('job1',jobs_lst,general_skill_for_job)

skill_for_different_level('job1','junior'
,jobs_lst,jobs_levels,skills_for_levels_jobs)

skill_for_different_level('job2','associate'
,jobs_lst,jobs_levels,skills_for_levels_jobs)

General skill input:  job
Skill for different level inpput:   job,level
"""

