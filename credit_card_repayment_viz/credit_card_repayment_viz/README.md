# 信用卡还款策略可视化

## 项目结构
- data/ : 银行利率数据
- src/ : 核心代码
- outputs/ : 生成的图片

## 运行方法
1. 创建 conda 环境：`conda create -n credit_env python=3.9`
2. 激活环境：`conda activate credit_env`
3. 安装依赖：`pip install -r requirements.txt`
4. 生成静态图：`cd src && python static_charts.py`
5. 运行交互网页：`cd src && streamlit run streamlit_app.py`