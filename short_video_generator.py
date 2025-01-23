import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip

# Function to crop frames to 9:16 aspect ratio
def crop_to_aspect_ratio(frame, aspect_ratio=(9, 16)):
    """
    Crop the input frame to the specified aspect ratio.
    Args:
        frame (ndarray): Frame to crop.
        aspect_ratio (tuple): Target aspect ratio as (width, height).
    Returns:
        Cropped frame.
    """
    height, width = frame.shape[:2]
    target_width = int(height * aspect_ratio[0] / aspect_ratio[1])
    x_start = (width - target_width) // 2
    return frame[:, x_start:x_start + target_width]

# Predefine interesting clips (start and end times in seconds)
clips_to_extract = [(5, 9), (15, 20), (35, 40)]  # Example clip ranges

# Step 1: Extract Clips
video_path = "input_video.mp4"
output_clips = []
for start, end in clips_to_extract:
    clip = VideoFileClip(video_path).subclip(start, end)
    # Crop to 9:16 aspect ratio
    cropped_clip = clip.crop(x_center=clip.w / 2, width=clip.h * 9 / 16, height=clip.h)
    output_clips.append(cropped_clip)

# Step 2: Add Music
music_path = "music.mp3"
music = AudioFileClip(music_path).set_duration(sum(clip.duration for clip in output_clips))

# Step 3: Add Text Overlays
final_clips = []
for idx, clip in enumerate(output_clips):
    # Create text overlay
    text = f"Scene {idx + 1}"
    text_overlay = TextClip(
        text, fontsize=50, color='white', font='Amiri-Bold'
    ).set_position('center').set_duration(clip.duration)
    
    # Combine video and text
    final_clip = CompositeVideoClip([clip, text_overlay])
    final_clips.append(final_clip)

# Step 4: Merge Clips and Export
final_video = concatenate_videoclips(final_clips, method="compose").set_audio(music)

# Export the video
output_path = "short_video.mp4"
final_video.write_videofile(output_path, fps=30, threads=4, codec="libx264")

print(f"Short video generated successfully and saved as {output_path}.")
