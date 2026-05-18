import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 导入利息计算函数（需要和本文件同一目录）
from interest_calculator import (
    min_payment_interest,
    installment_interest,
    full_payment_interest,
    annual_percentage_rate_from_monthly_fee,
)

st.set_page_config(page_title="信用卡还款策略对比", layout="wide")
st.title("💳 信用卡还款策略可视化")
st.markdown("比较 **最低还款**、**分期付款** 和 **全额还款** 的利息差异")

# ---------- 1. 读取银行利率 CSV ----------
csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "bank_rates.csv")
try:
    df_banks = pd.read_csv(csv_path)
    # 列名可能需要根据实际CSV调整，这里假定列名为：
    # 银行, 日利率, 最低还款比例, 分期3期费率, 分期6期费率, 分期12期费率, 滞纳金, 网址
    bank_names = df_banks["银行"].tolist()
except Exception as e:
    st.error(f"读取银行数据失败：{e}\n请确保 data/bank_rates.csv 文件存在且格式正确。")
    st.stop()

# ---------- 2. 侧边栏：选择银行 ----------
with st.sidebar:
    st.header("⚙️ 参数设置")
    selected_bank = st.selectbox("选择银行", bank_names)
    # 获取该银行的数据
    bank_row = df_banks[df_banks["银行"] == selected_bank].iloc[0]
    daily_rate = bank_row["日利率"]
    min_payment_ratio = bank_row["最低还款比例"]
    # 注意：最低还款比例可能是范围 "0.05-0.1"，这里简化取第一个值（可以改进）
    if isinstance(min_payment_ratio, str) and "-" in min_payment_ratio:
        min_ratio = float(min_payment_ratio.split("-")[0])
    else:
        min_ratio = float(min_payment_ratio)
    
    fee_3 = bank_row["分期3期费率"]
    fee_6 = bank_row["分期6期费率"]
    fee_12 = bank_row["分期12期费率"]
    
    st.caption(f"数据来源：{bank_row['网址']}")

# ---------- 3. 用户输入 ----------
amount = st.number_input("借款金额 (元)", min_value=500, max_value=50000, value=8000, step=500)
strategy = st.selectbox(
    "还款策略",
    ["最低还款（6个月）", "分期6期", "分期12期", "全额还款"],
)

# ---------- 4. 根据所选策略和银行利率计算利息 ----------
if strategy == "最低还款（6个月）":
    interest = min_payment_interest(amount, daily_rate, monthly_payment_ratio=min_ratio, max_months=6)
    extra_info = f"日利率 {daily_rate*100:.3f}%，每月还剩余本金 {min_ratio*100:.0f}%"
elif strategy == "分期6期":
    interest = installment_interest(amount, fee_6, 6)
    apr_est = annual_percentage_rate_from_monthly_fee(fee_6, 6)
    extra_info = f"每期费率 {fee_6*100:.2f}%，实际年化约 {apr_est}%"
elif strategy == "分期12期":
    interest = installment_interest(amount, fee_12, 12)
    apr_est = annual_percentage_rate_from_monthly_fee(fee_12, 12)
    extra_info = f"每期费率 {fee_12*100:.2f}%，实际年化约 {apr_est}%"
else:
    interest = 0.0
    extra_info = "无利息"

total_payment = amount + interest

# 显示核心指标
col1, col2 = st.columns(2)
col1.metric("总利息", f"{interest:.2f} 元")
col1.caption(extra_info)
col2.metric("总还款额", f"{total_payment:.2f} 元")

# ---------- 5. 对比所有策略（基于同一家银行的利率）----------
strategies_all = ["最低还款", "分期6期", "分期12期", "全额还款"]
interests_all = [
    min_payment_interest(amount, daily_rate, monthly_payment_ratio=min_ratio, max_months=6),
    installment_interest(amount, fee_6, 6),
    installment_interest(amount, fee_12, 12),
    0.0,
]
colors_all = ["#d62728", "#ff7f0e", "#ffbb78", "#2ca02c"]
fig = go.Figure(data=[go.Bar(x=strategies_all, y=interests_all, marker_color=colors_all)])
fig.update_layout(
    title=f"借款 {amount} 元各策略利息对比（{selected_bank}）",
    xaxis_title="还款策略",
    yaxis_title="利息 (元)",
)
st.plotly_chart(fig, use_container_width=True)

# ---------- 6. 债务递减曲线（仅最低还款）----------
if "最低还款" in strategy:
    with st.expander("📉 查看债务递减曲线（最低还款）"):
        balance = amount
        balances = [balance]
        for month in range(1, 13):
            if balance <= 1:
                balances.append(0)
                break
            interest_month = balance * daily_rate * 30
            payment = balance * min_ratio
            balance = balance - payment + interest_month
            balances.append(max(balance, 0))
        df_balance = pd.DataFrame({"月份": list(range(len(balances))), "剩余本金": balances})
        fig2 = go.Figure(data=go.Scatter(x=df_balance["月份"], y=df_balance["剩余本金"], mode="lines+markers"))
        fig2.update_layout(title="剩余本金变化曲线", xaxis_title="月份", yaxis_title="剩余本金 (元)")
        st.plotly_chart(fig2)

st.markdown("---")
# 假设前面已经计算了以下变量：
# amount: 用户输入的借款金额
# selected_bank: 当前选择的银行
# daily_rate: 日利率
# min_ratio: 最低还款比例
# fee_12: 12期每期费率

# 计算案例一：最低还款6个月利息
case1_interest = min_payment_interest(amount, daily_rate, monthly_payment_ratio=min_ratio, max_months=6)
# 计算案例二：分12期总手续费
case2_fee = installment_interest(amount, fee_12, 12)
case2_apr = annual_percentage_rate_from_monthly_fee(fee_12, 12)

st.subheader("🎓 校园真实场景示例")
st.info(
    f"""
    **案例一**：小明双十一买手机透支 **¥{amount:,.0f}**，选择**最低还款**（{selected_bank}），
    6个月后总利息约 **¥{case1_interest:.2f}**。  
    
    **案例二**：小华旅游消费 **¥{amount:,.0f}**，分12期还款（{selected_bank}），
    总手续费 **¥{case2_fee:.2f}**，实际年化利率约 **{case2_apr:.2f}%**。  
    
    **案例三**：小红坚持全额还款，利息为 **0** 元。
    """
)
st.caption(f"当前数据基于 {selected_bank} 的公开费率（{bank_row['网址']}）。实际以银行合同为准。")