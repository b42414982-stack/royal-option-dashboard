import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# إعدادات صفحة الداشبورد
st.set_page_config(
    page_title="Royal Option Dashboard V2",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Royal Option Dashboard V2")
st.markdown("لوحة تحليل الأسهم والخيارات الحية (محدثة مباشرة من السوق)")

# قائمة الأسهم المطلوبة (تتضمن SPY والأسهم الأخرى)
tickers_list = [
    "SPY", "QQQ", "AAPL", "MSFT", "NVDA", 
    "AMZN", "GOOGL", "META", "TSLA", "AMD"
]

st.sidebar.header("إعدادات العرض")
selected_ticker = st.sidebar.selectbox("اختر الرمز المالي (Ticker):", tickers_list)

# جلب بيانات السوق المباشرة
@st.cache_data(ttl=60)
def load_data(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="1mo")
    return data, hist

try:
    stock_data, hist_df = load_data(selected_ticker)
    
    # جلب السعر الحالي
    todays_data = stock_data.history(period="1d")
    if not todays_data.empty:
        current_price = todays_data['Close'].iloc[-1]
        prev_close = todays_data['Open'].iloc[-1]
        change = current_price - prev_close
        pct_change = (change / prev_close) * 100
        
        # عرض المؤشرات الحية في الأعلى
        col1, col2, col3 = st.columns(3)
        col1.metric("السعر الحالي", f"${current_price:.2f}", f"{change:.2f} ({pct_change:.2f}%)")
        col2.metric("أعلى سعر اليوم", f"${todays_data['High'].iloc[-1]:.2f}")
        col3.metric("أدنى سعر اليوم", f"${todays_data['Low'].iloc[-1]:.2f}")
    
    # عرض الرسم البياني لحركة السعر خلال شهر
    st.subheader(f"حركة السعر التاريخية لـ {selected_ticker} (آخر شهر)")
    st.line_chart(hist_df['Close'])
    
    # جدول البيانات التفصيلية
    st.subheader("بيانات الجلسة الأخيرة")
    st.dataframe(hist_df.tail(5))

except Exception as e:
    st.error(f"حدث خطأ أثناء جلب البيانات: {e}")
