
import streamlit as st
import os
import uuid
import cv2
import asyncio
import requests
from PIL import Image
import fitz, time, threading
from datetime import datetime
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import A4, A3, landscape
import winsound


if 'frame_count' not in st.session_state:
     st.session_state.frame_count=0

if 'video' not in st.session_state:
     st.session_state.video=False

if 'cap' not in st.session_state:
     st.session_state.cap=[]

if 'violation_pred' not in st.session_state:
     st.session_state.violation_pred=[]

if 'violation_pred_frame' not in st.session_state:
     st.session_state.violation_pred_frame=[]

if 'cap_web_cam' not in st.session_state:
     st.session_state.cap_web_cam=[]

if 'violation_pred_web_cam' not in st.session_state:
     st.session_state.violation_pred_web_cam=[]

if 'total_frames' not in st.session_state:
     st.session_state.total_frames=0

if 'all_frame' not in st.session_state:
     st.session_state.all_frame=0

if 'all_frame_2' not in st.session_state:
     st.session_state.all_frame_2=0

st.title("VisionGuardAI 🤖🎥📜")

# Create a PDF in memory
pdf_buffer = BytesIO()
c = canvas.Canvas(pdf_buffer)


def read_pdf_lines(pdf_path):
    lines = []
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text()
        lines.extend(text.splitlines())
    return lines

rules=[]

violated_frames = os.path.dirname(os.path.abspath(__file__))+"/Rules Violated Images/"

st.header ("📰 Upload Rules")

uploaded_file = st.file_uploader("**Choose a pdf file:**", type=["pdf"])
if st.button("Upload",key="pdf"):
    if uploaded_file is not None:
            
            unique_id = uuid.uuid4()
            output_directory = os.path.dirname(os.path.abspath(__file__))+'/uploads/'
            pdf_path = os.path.join(output_directory, str(unique_id)+'_'+uploaded_file.name)
            
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.session_state.rules=[]
            pdf_lines = read_pdf_lines(pdf_path)
            for line in pdf_lines:
                st.write(line)
                st.session_state.rules.append(line)
            
            

st.header ("🎥 Video Processing")

uploaded_file_video = st.file_uploader("**Choose a video:**", type=["mp4", "avi", "mov"])

if uploaded_file_video is None :
    st.session_state.video=False
    st.session_state.cap=[]
    st.session_state.violation_pred=[]
    st.session_state.total_frames=0
    st.session_state.frame_count=0
    

if st.button("Upload",key="Video"):
   if uploaded_file_video :
    st.session_state.video=True
    st.session_state.cap=[]
    st.session_state.violation_pred=[]
    st.session_state.total_frames=0
    st.session_state.frame_count=0


if st.session_state.video:
    if uploaded_file_video is not None:
        
        unique_id = uuid.uuid4()
        output_directory = os.path.dirname(os.path.abspath(__file__))+'/uploads/'
        video_path = os.path.join(output_directory, str(unique_id)+'_'+uploaded_file_video.name)
        
        with open(video_path, "wb") as f:
            f.write(uploaded_file_video.getbuffer())

        # Show video
        st.video(video_path)
        st.success("✅ Video uploaded successfully!")


        # Open the video file
        video = cv2.VideoCapture(video_path)
        st.session_state.total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        

        if not video.isOpened():
            st.write("Error: Could not open video.")
        else:
            # Get the frames per second (FPS)
            fps = video.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps)  # Capture 1 frame every second

            frame_count = 0
            saved_count = 0
            last_frame_count=st.session_state.get('frame_count')

            lines=[]
            for line in st.session_state.rules:
                st.write(line)
                lines.append(line.replace("\u200b", ""))
           
            prompt=""
            for line in lines:
                 prompt+=line+" "
           
            cap=st.session_state.cap
            violation_pred=st.session_state.violation_pred
            check=st.checkbox('Filter Violated Rules')
            f=0
            st.subheader("Rule-Violation Predictions:")

            while video.isOpened():
                ret, frame = video.read()
                if not ret:
                    break
                if frame_count>last_frame_count or st.session_state.frame_count==0:
                    if frame_count % frame_interval == 0:
                        # Encode frame as JPEG
                        _, encoded_frame = cv2.imencode('.jpg', frame)
                        frame_bytes = encoded_frame.tobytes()
                        with st.spinner('🌀 Analyzing video frames....'):
                            caption = requests.post(f"http://127.0.0.1/img_to_txt", files={"img": ("frame.jpg", frame_bytes, "image/jpeg")})
                            caption = caption.json()['txt']
                            
                        prompt2=prompt+" Caption: "+caption+""". Which rules have been violated in the caption according to the mentioned rules? If any rules get violated, mention those violated rules and explain the reason 25 words. If no rules are violated, then only say "No violation of rules." """
                        time_in_msec = video.get(cv2.CAP_PROP_POS_MSEC)
                        caption="Time-"+str(time_in_msec/1000)+": Scene description: "+caption
                        
                        if caption not in cap:
                            cap.append(caption)
                            with st.spinner('🌀 Rule violation status generating....'):
                                response = requests.get(f"http://127.0.0.1/prompt", params={"prompt":prompt2})
                            reply= response.json()['reply']
                            prediction="Rule violation status: "+reply
                            violation_pred.append(prediction)

                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            image = Image.fromarray(frame_rgb)
                            st.session_state.violation_pred_frame.append(image)
                            output_path = os.path.join(violated_frames,
                                                        f"{str(time_in_msec/1000)}.jpg")
                            image.save(output_path)

                        if check:
                             if not 'No violation of rules' in violation_pred[-1]:
                                    st.write(cap[-1])
                                    image = st.session_state.violation_pred_frame[-1]
                                    resized_image = image.resize((350, 250))
                                    with st.expander("Show Image"):
                                        st.image(resized_image,use_container_width=False)
                                    winsound.Beep(1000, 500)   
                                    st.success(violation_pred[-1])
                                    
                        else: 
                             st.write(cap[-1])
                             if not 'No violation of rules' in violation_pred[-1]:
                                    winsound.Beep(1000, 500)           
                             st.success(violation_pred[-1])
                             image = st.session_state.violation_pred_frame[-1]
                             resized_image = image.resize((350, 250))
                             with st.expander("Show Image"):
                                st.image(resized_image,use_container_width=False)  

                        st.session_state.frame_count=frame_count
                        st.session_state.cap=cap
                        st.session_state.violation_pred=violation_pred

                else:
                    if st.session_state.total_frames==st.session_state.frame_count:
                            for i in range(len(st.session_state.cap)):
                                if check:
                                    if not 'No violation of rules' in violation_pred[i]:
                                        st.write(cap[i])
                                        if i < len(violation_pred):
                                            image = st.session_state.violation_pred_frame[i]
                                            resized_image = image.resize((350, 250))
                                            with st.expander("Show Image"):
                                                st.image(resized_image,use_container_width=False)  
                                            st.success(violation_pred[i])
                                else: 
                                    st.write(cap[i]) 
                                    if i < len(violation_pred): 
                                        st.success(violation_pred[i])
                                        image = st.session_state.violation_pred_frame[i]
                                        resized_image = image.resize((350, 250))
                                        with st.expander("Show Image"):
                                            st.image(resized_image,use_container_width=False)  
                                        
                    else:
                        if f==0:
                            f=1
                            for i in range(len(st.session_state.cap)):
                                if check:
                                        if i < len(violation_pred):
                                            if not 'No violation of rules' in violation_pred[i]:
                                                st.write(cap[i])
                                                if i < len(violation_pred):
                                                    image = st.session_state.violation_pred_frame[i]
                                                    resized_image = image.resize((350, 250))
                                                    with st.expander("Show Image"):
                                                        st.image(resized_image,use_container_width=False)  
                                                    st.success(violation_pred[i])
                                else: 
                                        if i < len(violation_pred):
                                            st.write(cap[i]) 
                                            st.success(violation_pred[i])
                                            image = st.session_state.violation_pred_frame[i]
                                            resized_image = image.resize((350, 250))
                                            with st.expander("Show Image"):
                                                st.image(resized_image,use_container_width=False)       
                         
                frame_count += 1

            video.release()
            st.session_state.total_frames=st.session_state.frame_count
            


pdf_buffer = BytesIO()

c = canvas.Canvas(pdf_buffer, pagesize=(1000, 1400)) 

y = 1300  # start high on the page
c.drawString(50, y, "Report:",)
y -= 20
for i in range(len(st.session_state.cap)):
    c.drawString(50, y, st.session_state.cap[i],)
    y -= 20  # Move to next line
    if i < len(st.session_state.violation_pred):
        c.drawString(50, y, st.session_state.violation_pred[i])
    y -= 20  
c.save()
pdf_buffer.seek(0)  # Rewind the buffer

# Streamlit download button
st.download_button(
    label="Download Prediction Report",
    data=pdf_buffer,
    file_name="report.pdf",
    mime="application/pdf"
)

st.header("📷 Webcam Live Feed")

FRAME_WINDOW = st.image([])
video = None
web_cam_opended=False
start=st.checkbox("Start/Off Camera",key="Camera")

check=st.checkbox('Filter Violated Rules',key='ch')

pdf_buffer = BytesIO()

c = canvas.Canvas(pdf_buffer) 

y = 800  # start high on the page
c.drawString(50, y, "Report:",)
y -= 20
for i in range(len(st.session_state.cap_web_cam)):
    c.drawString(50, y, st.session_state.cap_web_cam[i])
    y -= 20  # Move to next line
    if(i<len(st.session_state.violation_pred_web_cam)):
        c.drawString(50, y, st.session_state.violation_pred_web_cam[i])
        y -= 20  
c.save()
pdf_buffer.seek(0)  
# Streamlit download button
st.download_button(
    label="Download Prediction Report",
    data=pdf_buffer,
    file_name="report.pdf",
    mime="application/pdf",
    key='d2',
)

if start:
    video = cv2.VideoCapture(0)
    frame_count=0
    frame_interval = video.get(cv2.CAP_PROP_FPS)
    lines=[]

    for line in st.session_state.rules:
        st.write(line)
        lines.append(line.replace("\u200b", ""))

    prompt=""
    for line in lines:
        prompt+=line+" "

    st.subheader("Rule-Violation Predictions:")
    while start:
        ret, frame = video.read()
        if not ret:
            st.warning("Failed to grab frame.")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)

        if frame_count % frame_interval == 0:
                    _, encoded_frame = cv2.imencode('.jpg', frame)
                    frame_bytes = encoded_frame.tobytes()
                    with st.spinner('🌀 Analyzing video frames....'):
                            caption = requests.post(f"http://127.0.0.1/img_to_txt", files={"img": ("frame.jpg", frame_bytes, "image/jpeg")})
                            caption = caption.json()['txt']
                    prompt2=prompt+" Caption: "+caption+""". Which rules have been violated in the caption according to the mentioned rules? If any rules get violated, mention those violated rules and explain the reason in 25 words. If no rules are violated, then only say "No violation of rules." """
                    time_in_msec = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    caption=str(time_in_msec)+": Scene description: "+caption
                    
                    if caption not in st.session_state.cap_web_cam:
                        st.session_state.cap_web_cam.append(caption)
                        with st.spinner('🌀 Rule violation status generating....'):
                                response = requests.get(f"http://127.0.0.1/prompt", params={"prompt":prompt2})
                        prediction="Rule violation status: "+ response.json()['reply']
                        st.session_state.violation_pred_web_cam.append(prediction)

                        frame_rgb = frame
                        image = Image.fromarray(frame_rgb)
                        st.session_state.violation_pred_frame.append(image)
                        img1="Image_"+str(len(st.session_state.cap_web_cam))
                        output_path = os.path.join(violated_frames,
                                                    f"{str(img1)}.jpg")
                        image.save(output_path)

                    if check:
                            if st.session_state.all_frame==0:
                                for i in range(len(st.session_state.violation_pred_web_cam)):
                                    if i < len(st.session_state.violation_pred_web_cam) and i<len(st.session_state.violation_pred_frame):
                                        if not 'No violation of rules' in st.session_state.violation_pred_web_cam[i]:
                                            st.write(st.session_state.cap_web_cam[i])
                                            st.success(st.session_state.violation_pred_web_cam[i])
                                            image = st.session_state.violation_pred_frame[i]
                                            resized_image = image.resize((350, 250))
                                            with st.expander("Show Image"):
                                                st.image(resized_image,use_container_width=False)
                                st.session_state.all_frame=1

                            elif st.session_state.all_frame==1:
                                if not 'No violation of rules' in st.session_state.violation_pred_web_cam[-1]:
                                    st.write(st.session_state.cap_web_cam[-1])
                                    winsound.Beep(1000, 500)            
                                    st.success(st.session_state.violation_pred_web_cam[-1])
                                    image = st.session_state.violation_pred_frame[-1]
                                    resized_image = image.resize((350, 250))
                                    with st.expander("Show Image"):
                                        st.image(resized_image,use_container_width=False)
                            st.session_state.all_frame_2=1
                                 
                    else:
                            if st.session_state.all_frame_2==1:
                                for i in range(len(st.session_state.violation_pred_web_cam)):
                                        if i < len(st.session_state.violation_pred_web_cam) and i<len(st.session_state.violation_pred_frame):
                                                st.write(st.session_state.cap_web_cam[i])
                                                st.success(st.session_state.violation_pred_web_cam[i])
                                                image = st.session_state.violation_pred_frame[i]
                                                resized_image = image.resize((350, 250))
                                                with st.expander("Show Image"):
                                                    st.image(resized_image,use_container_width=False)
                                st.session_state.all_frame_2=0
                            else: 
                                st.write(st.session_state.cap_web_cam[-1])
                                if not 'No violation of rules' in st.session_state.violation_pred_web_cam[-1]:
                                    winsound.Beep(1000, 500)            
                                st.success(st.session_state.violation_pred_web_cam[-1])
                                image = st.session_state.violation_pred_frame[-1]
                                resized_image = image.resize((350, 250))
                                with st.expander("Show Image"):
                                    st.image(resized_image,use_container_width=False)
                            
                            st.session_state.all_frame=0

        frame_count += 1
        web_cam_opended=True

if web_cam_opended:
    cap_web_cam=st.session_state.cap_web_cam
    violation_pred_web_cam=st.session_state.violation_pred_web_cam
    for i in range(len(st.session_state.cap_web_cam)):
        if check:
                if i < len(violation_pred_web_cam):
                    if not 'No violation of rules' in violation_pred_web_cam[i]:
                        st.write(cap_web_cam[i])
                        st.success(violation_pred_web_cam[i])
        else: 
                st.write(cap_web_cam[i]) 
                if i < len(violation_pred_web_cam):
                    st.success(violation_pred_web_cam[i])




