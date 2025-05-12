import streamlit as st
import pandas as pd

# 上传CSV文件
st.title("🌍 全球博士项目搜索器")
uploaded_file = st.file_uploader("请上传你爬好的CSV文件", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    st.success("数据加载成功！")
    st.write("预览前10条数据：")
    st.dataframe(df.head(10))

    # 搜索栏
    keyword = st.text_input("请输入关键词（研究方向、导师姓名、学校等）")

    # 筛选国家
    if "Country" in df.columns:
        country_list = df["Country"].dropna().unique().tolist()
        selected_country = st.selectbox("按国家筛选", ["全部"] + sorted(country_list))
    else:
        selected_country = "全部"

    # 过滤逻辑
    if keyword:
        df = df[df.astype(str).apply(lambda x: keyword.lower() in x.str.lower().to_string(), axis=1)]
    
    if selected_country != "全部":
        df = df[df["Country"] == selected_country]

    st.write(f"🔍 找到 {len(df)} 条匹配结果")
    st.dataframe(df)
