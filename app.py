import datetime
import streamlit as st
import random
import requests
import json
import pandas as pd

pages = st.sidebar.selectbox('Select page', ['user', 'room', 'booking'])

if pages == 'user':
    st.title('ユーザー登録画面')

    with st.form(key='user'):
        #user_id: int = random.randint(0, 10)
        user_name: str = st.text_input('ユーザ名', max_chars=10)
        data = {
            #'user_id': user_id,
            'user_name': user_name
        }
        submit_button = st.form_submit_button(label='送信')

    if submit_button:
        st.write('## レスポンス結果')
        url = 'http://127.0.0.1:8000/user'
        res = requests.post(url, data=json.dumps(data))
        if res.status_code == 200:
            st.success('ユーザー登録完了')
        st.write(res.status_code)
        st.error(res.json())
        
elif pages == 'room':
    st.title('ルーム登録画面')

    with st.form(key='room'):
        #room_id: int = random.randint(0, 10)
        room_name: str = st.text_input('ルーム名', max_chars=10)
        capacity: int = st.selectbox('人数', (1, 2, 3, 4, 5, 6))
        data = {
            #'room_id': room_id,
            'room_name': room_name,
            'capacity': capacity
        }
        submit_button = st.form_submit_button(label='送信')
    
    if submit_button:
        st.json(data)
        st.write('## レスポンス結果')
        url = 'http://127.0.0.1:8000/room'
        res = requests.post(url, data=json.dumps(data))
        if res.status_code == 200:
            st.success('登録完了')
        st.write(res.status_code)
        st.json(res.json())

elif pages == 'booking':
    st.title('予約登録画面')
    # ユーザー一覧取得
    url_user = 'http://127.0.0.0:8000/user'
    res = requests.get(url=url_user)
    users = res.json()
    users_dict = {}
    for user in users:
        users_dict[user['user_name']] = user['user_id']
    # ルーム一覧取得
    url_room = 'http://127.0.0.0:8000/room' 
    res = requests.get(url=url_room)
    rooms = res.json()
    rooms_dict = {}
    for room in rooms:
        rooms_dict[room['room_name']] = {
            'room_id': room['room_id'],
            'capacity': room['capacity']
        }
    
    st.write('## 会議室一覧')
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室ID']
    st.table(df_rooms)

    url_booking = 'http://127.0.0.0:8000/booking' 
    res = requests.get(url=url_booking)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)

    user_id = {}
    for user in users:
        user_id[user['user_id']] = user['user_name']
    room_id = {}
    for user in users:
        room_id[room['room_id']] = {
            'room_name': room['room_name'],
            'capacity': room['capacity'] 
        }

    # IDを各値に変換
    to_user_name = lambda x: user_id[x]
    to_room_name = lambda x: room_id[x]
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime('%y/%m/%d %H:%M')

    # 特定の列に適用
    df_bookings['user_id'] = df_bookings['user_id'].map(to_user_name)
    df_bookings['room_id'] = df_bookings['room_id'].map(to_room_name)
    df_bookings['start_datetime'] = df_bookings['start_datetime'].map(to_datetime)
    df_bookings['end_datetime'] = df_bookings['end_datetime'].map(to_datetime)

    df_bookings = df_bookings.rename(columns={
        'user_id': '予約者名',
        'room_id': '会議室名',
        'booking_num': '予約人数',
        'start_datetime': '開始日時',
        'end_datetime': '終了日時',
        'booking_id': '予約番号'
    })
    st.write('## 予約一覧')
    st.table(df_bookings)


    with st.form(key='booking'):
        user_name: str = st.selectbox('予約者名', users_dict.keys())
        room_name: str = st.selectbox('会議室名', rooms_dict.keys())
        #booking_id: int = random.randint(0, 100)
        user_id: int = random.randint(0, 10)
        room_id: int = random.randint(0, 10)
        booking_num: str = st.number_input('予約人数', step=1, min_value=1)
        date = st.date_input('日付:', min_value=datetime.date.today())
        start_time = st.time_input('開始時刻:', value=datetime.time(hour=9, minute=0)) 
        end_time = st.time_input('終了時刻:', value=datetime.time(hour=10, minute=0)) 
        submit_button = st.form_submit_button(label='送信')
    
    if submit_button:
        user_id: int = users_dict[user_name]
        room_id: int = rooms_dict[room_name]['room_id']
        capacity: int = rooms_dict[room_name]['capacity'] 
        data = {
            #'booking_id': booking_id,
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
        if booking_num <= capacity:
            url = 'http://127.0.0.1:8000/booking'
            res = requests.post(url, data=json.dumps(data))
            if res.status_code == 200:
                st.success('予約完了')
            st.json(res.json())
        else:
            st.error(f'{room_name}の定員は、{capacity}名までです。')