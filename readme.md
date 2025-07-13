# VisionGuardAI: A Streamlit & FastAPI App for Rule-Based Anomaly Detection from CCTV and Uploaded Video 🎥📜🧠⚖️

A surveillance-aware AI application powered by Streamlit and FastAPI for intelligent anomaly detection using video streams (CCTV, live feed, or uploads), uploaded video, and rule documents (PDF).
---

## 🔍 Overview

**VisionGuardAI** empowers users to detect rule violations in videos or live camera footage by combining advanced computer vision techniques with powerful language models. The system analyzes frames, generates natural-language descriptions, and evaluates them against uploaded rulebooks to detect anomalies, featuring automatically flagging violations and saving critical evidences.

It allows users to upload a rule document (PDF) and a video, or enables users to utilize live camera feeds. The system extracts frames per second, generates descriptive captions for each frame using a vision to text model (BLIP), and evaluates these captions against the uploaded rules using a large language model (LLaMA). Extracted frames are saved with a timestamp in a folder named 'Rule Violated Images'. When violations are detected, they are identified along with explanations and corresponding timestamps. The application also emits a beep sound whenever a rule violation is detected, providing immediate audio feedback. Users can filter the results to view only the data related to rule violations and download a PDF report containing all scene descriptions along with their corresponding rule violation evaluations. 

---

## 🎯 Key Features

### 📥 Rule Upload (PDF)
- Upload a rulebook in PDF format.
- Rules are parsed and converted to a structured format for LLM processing.

### 🎞️ Video Analysis
- Upload a video or stream live from a camera.
- Extract frames at 1-second intervals.
- Generate natural language captions using BLIP.
- Evaluate captions against uploaded rules using an LLM (LLaMA).
- Identify and tag rule violations in real time.

### 🚨 Rule Violation Detection
- Clearly mark frames and timestamps where rule violations occur.
- Display violated rule(s) and the reason behind the violation.
- Plays a beep sound instantly upon detecting a rule violation.

### 🖼️ Visual Dashboard
- Display frame snapshots for visual context.
- View all frame captions with violation predictions and timestamps.
- Filter to show only rule-violated frames and corresponding data.

### 📄 Report Generation
- Generate and download a comprehensive report containing:
  - All frames with scene descriptions and violation detections.
  - Include timestamps against the predictions

### 💾 Data Persistence
- Save images of each frame (once per second) with a timestamp.
- Option to export all frames, captions, and violation analysis.

---

## 📸 UI Preview
![0_0_0](https://github.com/user-attachments/assets/19d83845-9eee-4103-948b-e311194c4294)
![UI Image-1](https://github.com/user-attachments/assets/07f80a3f-bae2-424a-b940-ac32e27ada66)
![UI Image-2](https://github.com/user-attachments/assets/b45a9ee1-5283-45d0-a87e-09ac301c84ba)
![UI Image-3](https://github.com/user-attachments/assets/81de4bd8-2d8c-40a8-8c74-b9ff2c226db1)
![UI Image-4](https://github.com/user-attachments/assets/88ebce16-654b-4707-9864-f971b5d72dd0)
![UI Image-5](https://github.com/user-attachments/assets/959c978d-1174-498c-8848-8ac0eb54b202)
![UI Image-6](https://github.com/user-attachments/assets/ce29683e-a3ed-406d-a7ef-e68aee0d6b86)
![UI Image-7](https://github.com/user-attachments/assets/86960a89-a4b1-421e-bdc6-8fc4e2e8f143)
![UI Image-8](https://github.com/user-attachments/assets/7533fb3c-6ed0-4385-b889-daae26a9a28b)

---

## ▶️ How to Run
1. Clone the Repository

```bash
git clone https://github.com/NxtVis/vision-prito/VisionGuardAI Rule-based Anomaly Detection_BLIP_Llama.git
cd VisionGuardAI Rule-based Anomaly Detection_BLIP_Llama
```
2. Create and Activate a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```
3. Install Required Packages
```bash
pip install -r requirements.txt
```
4. Start the FastAPI Backend
```bash
cd server
python fstapi.py
```
5. Launch the Streamlit App
```bash
streamlit run app.py
```
---

## 🚧 Scope and Limitations

### ✅ Scope:
- Integrated platform for rule-based anomaly detection in video using computer vision and LLMs.
- Supports both uploaded videos and real-time camera feeds.
- Frame-level scene analysis and violation detection using vision-to-text captioning and rule evaluation.
- Allows uploading and parsing of PDF-based rulebooks.
- Provides an intuitive Streamlit dashboard for visual inspection and filtering.
- Enables exporting of violations and full detection logs as PDF reports.
- Useful for security, compliance monitoring, and automated surveillance analysis.

### ⚠️ Limitations:
- Currently supports:
  - **PDF** for rule input.
  - **.mp4** for video files.
- Frame extraction is set at **1 frame per second**—fast motion may be partially missed.
- Captioning accuracy depends on the BLIP model’s understanding of complex scenes.
- LLM evaluation may vary in quality based on model (e.g., LLaMA, GPT).
- No real-time alerting system (e.g., SMS/email) implemented yet.
- Requires moderate to high system resources (CPU/GPU) for smooth performance.
- No database integration or long-term data persistence.
- Assumes clearly written, structured rules in the PDF for accurate parsing.

---

## 🎯 Future Targets

- 📡 Support for **multi-camera streams** and multi-angle analysis.
- 📤 Integration with **alert systems** (email, SMS, webhook) for real-time notifications.
- 🧠 Use of **fine-tuned domain-specific LLMs** for more accurate violation detection.
- 💽 Add **database support** (PostgreSQL, MongoDB) for persistent storage of frames, captions, and violation logs.
- ☁️ Enable **cloud deployment** with Docker and Kubernetes for scalable usage.
- 🔐 Implement **user authentication and role-based access control** for secure multi-user environments.
- 📊 Add **violation statistics dashboards** with charts, heatmaps, and trends.
- 🛠️ Incorporate **adaptive frame extraction** based on motion/activity rather than fixed intervals.
- 🖇️ Add in-app **rule editor** to modify or add rules post-upload.
