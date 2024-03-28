import hashlib
import json
from openai import OpenAI
import os
import requests
import sys
import traceback
import uuid
from dotenv import load_dotenv
import csv

load_dotenv()


# Create the output directory if it doesn't exist
output_directory = "./output"
audio_directory = output_directory + "/audio"
transcript_directory = output_directory + "/transcripts"


download_api_url = "https://co.wuk.sh/api/json"
download_api_request_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def makeAudioFile(video_url, mp3_file_path):
    mp3_download_response = requests.post(
            download_api_url,
            headers=download_api_request_headers,
            json={
                "url": video_url,
                "isAudioOnly": "true"
            }
    )
    print(mp3_download_response.text)
    exit()
    mp3_download_response.raise_for_status()
    mp3_download_data = mp3_download_response.json()
    
    mp3_download_url = mp3_download_data['url']
    
    mp3_audio_response = requests.get(mp3_download_url)
    mp3_audio_response.raise_for_status()
    mp3_audio_data = mp3_audio_response.content

    with open(mp3_file_path, "wb") as file:
        file.write(mp3_audio_data)
    
    print("Audio file created successfully!")



def getTranscript(mp3_file_path):
    
    client = OpenAI()
    audio_file= open(mp3_file_path, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    print(transcription)

    transcript_string = transcription.text

    # Add a carriage return after each question mark or each dot and a space
    transcript_string = transcript_string.replace("?", "?\n")
    transcript_string = transcript_string.replace(".", "\n")

    return transcript_string



def processVideo(video_url):

    file_uuid = uuid.uuid5(uuid.NAMESPACE_URL, hashlib.md5(video_url.encode('utf-8')).hexdigest())

    mp3_file_name = f"{file_uuid}.mp3"
    mp3_file_path = os.path.join(audio_directory, mp3_file_name)
    if os.path.exists(mp3_file_path):
        print("Using cached audio file...")
    else:
        print("Using audio download API...")
        try:
            makeAudioFile(video_url, mp3_file_path)
        except requests.exceptions.HTTPError as e:
            print("Audio file download call failed with error:", str(e))
        except:
            print("An unexpected error occured:")
            traceback.print_exc()

    
    try:
        return getTranscript(mp3_file_path)
    except:
        print("An unexpected error occured:")
        traceback.print_exc()
        return


def processChannel():

    from fpdf import FPDF 
    import csv
    import os

    pdf = FPDF()

    with open('input/urls.csv', newline='',errors="ignore") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        for row in reader:
            print(row)
            
            try:

                video_desc = row[0].encode('latin1').decode('utf-8')
                video_url = row[1]
                video_transcript = processVideo(video_url)

                # Test if video_desc and video_transcript are not empty and not null

                if video_desc and video_transcript:

                    pdf.add_page()
                    pdf.add_font('Arial', '', 'c:/windows/fonts/arial.ttf', uni=True)  # added line
                    pdf.set_font('Arial', '', 8)
                    
                    pdf.cell(0, 10, "Description de la vidéo", 0, 1, 'C')
                    for sentence in video_desc.split('.'):
                        pdf.cell(0, 5, sentence + ".", 0, 1)
                        pdf.ln()
                    
                    pdf.cell(0, 10, "Script", 0, 1, 'C')
                    pdf.multi_cell(0, 5, video_transcript)

            except Exception as e:
                pass

    pdf.output("output/transcripts/transcript.pdf")


        
        






if __name__ == '__main__':
  
    processChannel()
    
    
    
