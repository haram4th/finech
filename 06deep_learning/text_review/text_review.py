import gradio as gr
import tensorflow as tf
import numpy as np
import joblib
import os
import sys
import re
from konlpy.tag import Okt
okt = Okt()

 # GPU 무시하고 CPU만 사용
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# 모델 및 구성 로드
model = tf.keras.models.load_model("./model/bank_app_review_attn_model.keras")
tokenizer = joblib.load("./model/bank_app_tokeizer.joblib")
max_len = joblib.load("./model/bank_app_max_length.joblib")


# 텍스트 정제
def clean_text(text):
    cleaned = re.sub(r'[^가-힣a-zA-Z0-9\s]','', text) #한글, 영문, 숫자
    cleaned = re.sub(r'\s+', ' ', cleaned) # 연속된 공백을 하나의 공백
    return cleaned.strip()


# 감성 분석 함수
def predict_sentiment(text):
    cleaned_text = clean_text(text)
    tokenized_text = okt.morphs(cleaned_text)
    seq = tokenizer.texts_to_sequences(tokenized_text)
    padded = tf.keras.preprocessing.sequence.pad_sequences(seq, maxlen=max_len, padding='post', truncating='post')
    pred = model.predict(padded)[0][0]
    label = "긍정 😊" if pred >= 0.5 else "부정 😞"
    return f"{label} (확률: {pred:.2f})"

# Gradio 앱
demo = gr.Interface(
    fn=predict_sentiment,
    inputs=gr.Textbox(lines=4, placeholder="은행 앱 리뷰를 입력하세요"),
    outputs="text",
    title="💬 은행 앱 감성 분석기 (Attention 기반)",
    description="입력한 리뷰 문장이 긍정적인지 부정적인지 분석합니다."
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
