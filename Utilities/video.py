from youtube_transcript_api import YouTubeTranscriptApi  
  
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

