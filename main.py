from fastapi import FastAPI, UploadFile, Form
# from fastapi.responses import FileResponse
from moviepy.editor import *
import json
import os

app = FastAPI()


@app.post("/upload")
async def upload_files(videos: list[UploadFile], videoJson: str = Form(...)):
    video_json = json.loads(videoJson)

    for clip in video_json['clips']:
        filename = clip['videoUrl']
        for video in videos:
            if video.filename == filename:
                await process_video(video, clip['operations'])


    # Further code to handle final composition and output
    # ...

    return {"message": "Processing Complete"}


async def process_video(video_file, operations):
    # Save the file temporarily
    temp_file_path = f'temp_{video_file.filename}'
    with open(temp_file_path, 'wb') as f:
        content = await video_file.read()
        f.write(content)

    # Process the video
    video = VideoFileClip(temp_file_path)

    # Apply operations
    for op in operations:
        if op['action'] == 'subclip':
            video = video.subclip(op['start'], op['end'])
        elif op['action'] == 'resize':
            video = video.resize(newsize=(op['width'], op['height']))
        # Add more operations as needed

    # Save the processed video
    output_path = f'processed_{video_file.filename}'
    video.write_videofile(output_path)

    # Clean up
    video.close()
    # os.remove(temp_file_path)


# Additional functions for final composition and sending files
# ...

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
