import streamlit as st
import requests
import re
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# 1. 고도화된 스타일 설정 (캐싱 및 에러 방지 추가)
st.set_page_config(page_title="다나와 PRO 클론", layout="wide", page_icon="🛒")

# CSS 최적화: 가독성 및 모바일 대응 보완
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .product-card {
        background: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 20px;
        border-left: 6px solid #0056b3; transition: transform 0.2s;
    }
    .product-card:hover { transform: translateY(-2px); }
    .price-large { color: #d32f2f; font-size: 28px; font-weight: 800; }
    .badge { background: #0056b3; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .mall-info { color: #666; font-size: 14px; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)
git : 'git' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다. 이름이 정확한지 확인하고 경로가 포함된 경우 경로가 올바른지 검증한 다음 다시 시도하십시오.
위치 줄:1 문자:1
+ git --version
+ ~~~
    + CategoryInfo          : ObjectNotFound: (git:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
# 2. 핵심 유틸리티 함수 (에러 핸들링 강화)
def clean_html(raw_html):
    return re.sub('<.*?>', '', raw_html) if raw_html else "이름 없음"

@st.cache_data(ttl=3600) # API 호출 결과 1시간 동안 캐싱 (속도 향상)
def get_api_data(query, display=30, sort='sim', start=1):
    # Secrets 체크 (배포 시 에러 방지)
    if "NAVER_CLIENT_ID" not in st.secrets:
        st.error("API 키가 설정되지 않았습니다. .streamlit/secrets.toml 파일을 확인하세요.")
        return None
        
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": st.secrets["NAVER_CLIENT_ID"],
        "X-Naver-Client-Secret": st.secrets["NAVER_CLIENT_SECRET"]
    }
    params = {"query": query, "display": display, "start": start, "sort": sort}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류 발생: {e}")
        return None

# 3. 세션 상태 초기화
for key in ['wishlist', 'compare_pool', 'search_query']:
    if key not in st.session_state:
        st.session_state[key] = "" if key == 'search_query' else []

# --- 사이드바: 다나와식 상세 필터링 ---
with st.sidebar:
    # 로고 이미지 예외 처리
    logo_url = "https://img.danawa.com/new/tour/img/logo/danawa_logo.png"
    try:
        st.image(logo_url, width=150)
    except:
        st.title("🏙️ DANAWA PRO")
    
    st.title("⚙️ 상세 필터")
    sort_mode = st.selectbox("정렬 기준", ["sim", "asc", "dsc", "date"], 
                             format_func=lambda x: {"sim":"추천순", "asc":"최저가순", "dsc":"최고가순", "date":"최신순"}[x])
    
    price_range = st.slider("가격대 설정 (만원)", 0, 1000, (0, 500))
    
    st.divider()
    st.subheader("⭐ 마이 페이지")
    col_w, col_c = st.columns(2)
    col_w.metric("찜", f"{len(st.session_state.wishlist)}개")
    col_c.metric("비교", f"{len(st.session_state.compare_pool)}개")
    
    if st.button("🗑️ 전체 데이터 초기화", use_container_width=True):
        st.session_state.wishlist, st.session_state.compare_pool = [], []
        st.rerun()

# --- 메인 화면 ---
st.title("🏢 가격비교의 끝, DANAWA PRO")

# 퀵 카테고리 (버튼 디자인 개선)
cats = ["💻 노트북", "📱 스마트폰", "🎮 그래픽카드", "🎧 헤드셋", "📺 TV"]
c_cols = st.columns(len(cats))
for idx, c in enumerate(cats):
    if c_cols[idx].button(c, use_container_width=True):
        st.session_state.search_query = c.split()[-1]
        st.rerun()

main_search = st.text_input("상품 검색", value=st.session_state.search_query, 
                            placeholder="모델명이나 상품명을 입력하세요 (예: 맥북 에어 M3)", 
                            label_visibility="collapsed")

if main_search:
    with st.spinner('최저가를 찾는 중...'):
        data = get_api_data(main_search, sort=sort_mode)
    
    if data and 'items' in data and len(data['items']) > 0:
        t_list, t_analysis, t_wish = st.tabs(["🔍 검색 결과", "📈 가격 통계", "❤️ 찜/비교함"])
        
        with t_list:
            for item in data['items']:
                price = int(item['lprice'])
                if not (price_range[0]*10000 <= price <= price_range[1]*10000): continue
                
                title = clean_html(item['title'])
                
                with st.container():
                    st.markdown(f"""
                    <div class="product-card">
                        <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                            <img src="{item['image']}" style="width: 180px; height: 180px; object-fit: contain; border-radius: 8px; background: #fff;">
                            <div style="flex: 1; min-width: 300px;">
                                <span class="badge">{item.get('category3', '카테고리')}</span>
                                <h3 style="margin: 10px 0; color: #333;">{title}</h3>
                                <p class="mall-info">🏢 {item['mallName']} | 제조사: {item.get('maker', '정보없음')}</p>
                                <p class="price-large">{format(price, ',')}원</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    b1, b2, b3, _ = st.columns([1.2, 1, 1, 3])
                    b1.link_button("🌐 최저가 구매처", item['link'], use_container_width=True)
                    if b2.button("❤️ 찜하기", key=f"wish_{item['productId']}"):
                        if item not in st.session_state.wishlist: 
                            st.session_state.wishlist.append(item)
                            st.toast(f"'{title[:10]}...' 상품을 찜했습니다!")
                    if b3.button("⚖️ 비교담기", key=f"comp_{item['productId']}"):
                        if item not in st.session_state.compare_pool: 
                            st.session_state.compare_pool.append(item)
                            st.toast("비교함에 추가되었습니다.")
                    st.write("") # 간격 조절

        with t_analysis:
            st.subheader("📊 가격 데이터 리포트")
            prices = [int(i['lprice']) for i in data['items']]
            
            c1, c2, c3 = st.columns(3)
            c1.metric("검색 평균가", f"{format(int(np.mean(prices)), ',')}원")
            c2.metric("최저가", f"{format(min(prices), ',')}원", delta=f"-{format(int(np.mean(prices)-min(prices)), ',')}", delta_color="normal")
            c3.metric("최고가", f"{format(max(prices), ',')}원")

            # 시각화
            fig_hist = px.histogram(prices, nbins=15, title="현재 검색 결과 가격 분포", 
                                   labels={'value':'가격(원)'}, color_discrete_sequence=['#0056b3'])
            st.plotly_chart(fig_hist, use_container_width=True)

        with t_wish:
            if st.session_state.compare_pool:
                st.subheader("⚖️ 선택 상품 제원 비교")
                comp_df = pd.DataFrame([
                    {"상품명": clean_html(i['title']), "가격": int(i['lprice']), "판매처": i['mallName'], "카테고리": i['category3']} 
                    for i in st.session_state.compare_pool
                ])
                st.dataframe(comp_df, use_container_width=True)
                fig_comp = px.bar(comp_df, x="상품명", y="가격", text_auto='.2s', title="비교 상품 가격 대조")
                st.plotly_chart(fig_comp, use_container_width=True)
            else:
                st.info("비교함이 비어있습니다. 상품 리스트에서 '비교담기'를 눌러주세요.")
    else:
        st.warning("검색 결과가 없습니다. 다른 키워드로 검색해 보세요.")
else:
    st.info("💡 위 검색창에 상품을 입력하거나 퀵 메뉴를 눌러 쇼핑을 시작하세요!")