#!/usr/bin/env python
# coding: utf-8

# In[16]:


api_key = input('Enter your YouTube API Key:')


# In[1]:


import urllib.request
import json
from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
import pickle 


# In[2]:


# put in channel_id, returns all video_id and video_links

def get_all_video_in_channel(api_key, channel_id):
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key, channel_id)
    video_links = []
    video_id=[]
    url = first_url
    while True:
        inp = urllib.request.urlopen(url,timeout=1)
        resp = json.load(inp)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(base_video_url + i['id']['videoId'])
                video_id.append(i['id']['videoId'])
        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_id, video_links


# In[3]:


video_ids, video_links=get_all_video_in_channel(api_key,'UCNvsIonJdJ5E4EXMa65VYpA')


# In[8]:


yt=YouTube('https://www.youtube.com/watch?v=aPWLO4wMCjU&t=1s')
captions=yt.captions['a.en']
type(captions)


# In[9]:


from pytube import YouTube
def transcript(video_link):
    source=YouTube(video_link)
    en_caption = source.captions['en']
    if en_caption is None:
        en_caption=source.captions['a.en']
    if en_caption is None:
        return f'{video_link} does not have caption.'
    
    en_caption_convert_to_srt =(en_caption.generate_srt_captions())
    #save the caption to a file named Output.txt
    text_file = open(video_link[-11:]+".txt", "w",encoding='utf-8')
    text_file.write(en_caption_convert_to_srt)
    text_file.close()
    # read file line by line
    with open(video_link[-11:]+".txt",'r',encoding='utf-8') as file:
        lines=file.readlines()
        text=''
        for i, line in enumerate(lines):
            if ' --> ' in line:
                text+=' '+lines[i+1].rstrip('\n')
            else:
                continue
        return text    


# In[7]:


len(transcript)


# In[10]:


import os
os.mkdir('contra-transcripts')


# In[14]:


for i, video_id in enumerate(video_ids):
    with open(video_id + ".txt", "wb") as file:       
        pickle.dump(transcript[i], file)        


# In[16]:


data={}
for i, video_id in enumerate(video_ids):
    with open(video_id + ".txt", "rb") as file:       
        data[i]=pickle.load(file)
            
        


# In[17]:


data


# In[10]:


def srt_to_text(file_name):
with open(file_name,'r',encoding='utf-8') as file:
    lines=file.readlines()
    text=''
    for i, line in enumerate(lines):
        if ' --> ' in line:
            text+=' '+lines[i+1].rstrip('\n')
        else:
            continue
    return text


# In[21]:


#download the package by:  pip install pytube
from pytube import YouTube
source = YouTube('https://www.youtube.com/watch?v=vRBsaJPkt2Q')
en_caption = source.captions['en']
en_caption_convert_to_srt =(en_caption.generate_srt_captions())
#print(en_caption_convert_to_srt)
#save the caption to a file named Output.txt
text_file = open("Output.srt", "w", encoding='utf-8')
text_file.write(en_caption_convert_to_srt)
text_file.close()

import re
def srt_to_text(file_name):
    # read file line by line
    file = open(file_name, 'r', encoding='utf-8')
    lines = file.readlines()
    file.close()

    text = ''
    for line in lines:
        if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
            text += ' ' + line.rstrip('\n')
        text = text.lstrip()
    return text

srt_to_text("Output.srt")


# In[7]:


# pip install youtube_transcript_api


# In[43]:


for i in video_id:
    data=yta.get_transcript(i, languages=['en'])
    transcript=''
    for value in data:
        for key,val in value.items():
            if key=='text':
                transcript+=val
    l=transcript.splitlines()
    final_t=" ".join(l)
    print(final_t)


# In[46]:


bad_id=[]
for i in video_id:
    try:
        data=yta.get_transcript(i, languages=['en'])
        transcript=''
        for value in data:
            for key,val in value.items():
                if key=='text':
                    transcript+=val
        l=transcript.splitlines()
        final_t=" ".join(l)
    except:
        print(i+' did not work')
        bad_id.append(i)


# In[47]:


final_t


# In[ ]:




