from youtube_transcript_api import YouTubeTranscriptApi  
import os
  
def get_youtube_transcript(video_id):  
    transcript = YouTubeTranscriptApi.get_transcript(video_id)  
    text = ""  
  
    for sentence in transcript:  
        text += sentence['text'] + " "  
  
    return text  

import re  
  
def parse_youtube_link(message):  
    youtube_regex = r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"  
    youtube_url = re.search(youtube_regex, message)  
      
    if youtube_url:  
        return youtube_url.group()  
    else:  
        return None  


def create_transcript_if_not_exists(video_id):
    file_path = f"Data/{video_id}.txt"
    print(f"\n\n file_path: {file_path} \n\n ")

    if os.path.exists(file_path):  
        # Read the transcript from the existing file  
        with open(file_path, "r") as file:  
            transcript = file.read()
    else:
        with open(file_path, 'w') as f:  
            transcript = get_youtube_transcript(video_id)
    
    return transcript
