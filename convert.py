import json, yaml

with open('D:\\PPMBot\\Clai2_Knowledge_Collection.json') as f:
    data = json.load(f)
    
#ques=data.get("faqs")[0]

i=0

for ques in data.get("faqs"):
    i=i+1
    
    #Reading the question (intent)
    intentName="kb_"+str(i)
    quesLine="\n## intent:"+intentName+"\n- "+ques.get("question")+"\n"
    
    for q in ques.get("alternateQuestions"):
        quesLine=quesLine+"- "+q.get("question")+"\n"
    
    #print(quesLine)
    #writing intent to nlu.md
    fw=open('D:\\rasa\\clai\\data\\nlu.md','a')
    fw.writelines(quesLine)
    fw.close()
    
    #Reading the answer (bot response)
    altAns=ques.get("alternateAnswers")[0]
    text=""
    gotAns=0
    for ans in altAns:
        if ans.get("type")=="basic":
            gotAns=1
            text=ans.get("text")
    if gotAns==0:
        text=ques.get("answer")[0].get("text")
        
    #Reading existing content of domain.yml
    fr=open('D:\\rasa\\clai\\domain.yml','r')
    domainData=yaml.load(fr, Loader=yaml.FullLoader)
    fr.close()
    
    #Writing intent and response to the domain:
    domain={}
    for item in domainData:
        if item=="intents":
            obj=domainData.get("intents")
            obj.append(intentName)
        elif item=="responses":
            obj=domainData.get("responses")
            obj.update({"utter_"+intentName:[{"text":text}]})
        else:
            obj=domainData.get(item)
        domain.update({item:obj})
        
    with open('D:\\rasa\\clai\\domain.yml', 'w') as fw:
        document=yaml.dump(domain, fw)
    fw.close()
    
    #Writing stories
    fstories=open('D:\\rasa\\clai\\data\\stories.md','a')
    story="\n## loaded_story_1_"+intentName+"\n"
    story=story+"* "+intentName+"\n"
    story=story+"  - utter_kb_init_txt\n"
    story=story+"  - utter_"+intentName+"\n"
    story=story+"  - utter_feedback\n"
    story=story+"* helpful\n"
    story=story+"  - utter_happy\n"
    story=story+"\n## loaded_story_2_"+intentName+"\n"
    story=story+"* "+intentName+"\n"
    story=story+"  - utter_kb_init_txt\n"
    story=story+"  - utter_"+intentName+"\n"
    story=story+"  - utter_feedback\n"
    story=story+"* not_helpful\n"
    story=story+"  - utter_not_helpful\n"
    story=story+"* affirm\n"
    story=story+"  - utter_post_feedback\n"
    fstories.writelines(story)
    fstories.close()

f.close()