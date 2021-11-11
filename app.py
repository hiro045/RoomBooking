import datetime
import streamlit as st
import random
import requests
import json

pages = st.sidebar.selectbox('Select page', ['user', 'room', 'booking'])

if pages == 'user':
    st.title('APIテスト画面(ユーザー)')

    with st.form(key='user'):
        user_id: int = random.randint(0, 10)
        user_name: str = st.text_input('ユーザ名', max_chars=10)
        data = {
            'user_id': user_id,
            'user_name': user_name
        }
        submit_button = st.form_submit_button(label='送信')

    if submit_button:
        st.write('## 送信データ')
        st.json(data)
        st.write('## レスポンス結果')
        url = 'http://127.0.0.1:8000/user'
        res = requests.post(url, data=json.dumps(data))
        st.json(res.json())
elif pages == 'room':
    st.title('APIテスト画面(ルーム)')

    with st.form(key='room'):
        room_id: int = random.randint(0, 10)
        room_name: str = st.text_input('ルーム名', max_chars=10)
        capacity: int = st.selectbox('人数', (1, 2, 3, 4, 5, 6))
        data = {
            'room_id': room_id,
            'room_name': room_name,
            'capacity': capacity
        }
        submit_button = st.form_submit_button(label='送信')
    
    if submit_button:
        st.write('## 送信データ')
        st.json(data)
        st.write('## レスポンス結果')
        url = 'http://127.0.0.1:8000/room'
        res = requests.post(url, data=json.dumps(data))
        st.json(res.json())
elif pages == 'booking':
    st.title('APIテスト画面(予約)')

    with st.form(key='booking'):
        booking_id: int = random.randint(0, 100)
        user_id: int = random.randint(0, 10)
        room_id: int = random.randint(0, 10)
        booking_num: str = st.number_input('予約人数', step=1)
        date = st.date_input('日付:', min_value=datetime.date.today())
        start_time = st.time_input('開始時刻:', value=datetime.time(hour=9, minute=0)) 
        end_time = st.time_input('終了時刻:', value=datetime.time(hour=10, minute=0)) 
        submit_button = st.form_submit_button(label='送信')
        data = {
            'booking_id': booking_id,
            'user_id': user_id,
            'room_id': room_id,
            'booking_num': booking_num,
            'start_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute
            ).isoformat(),
            'end_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute
            ).isoformat() 
        }
    
    if submit_button:
        st.write('## 送信データ')
        st.json(data)
        st.write('## レスポンス結果')
        url = 'http://127.0.0.1:8000/booking'
        res = requests.post(url, data=json.dumps(data))
        st.json(res.json())