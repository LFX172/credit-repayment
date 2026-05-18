import matplotlib.pyplot as plt
import os
import sys
# 将当前目录加入路径，以便导入 interest_calculator
sys.path.append(os.path.dirname(__file__))
from interest_calculator import min_payment_interest, installment_interest, full_payment_interest

# 利率参数（可以从 CSV 读取，但这里先手动设定）
DAILY_RATE = 0.0005
MONTHLY_FEE_6 = 0.008
AMOUNTS = [3000, 8000, 15000]
STRATEGIES = ["最低还款", "分期6期", "全额还款"]
COLORS = ["#d62728", "#ff7f0e", "#2ca02c"]

def create_static_charts():
    # 确保 outputs 目录存在（相对于项目根目录）
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    for i, principal in enumerate(AMOUNTS):
        interests = [
            min_payment_interest(principal, DAILY_RATE, max_months=6),
            installment_interest(principal, MONTHLY_FEE_6, 6),
            full_payment_interest(),
        ]
        axes[i].bar(STRATEGIES, interests, color=COLORS)
        axes[i].set_title(f"借款 {principal} 元")
        axes[i].set_ylabel("总利息 (元)")
        for j, val in enumerate(interests):
            axes[i].text(j, val + 5, f"{val:.0f}", ha="center", fontsize=9)
    
    plt.tight_layout()
    save_path = os.path.join(output_dir, "static_comparison.png")
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"静态对比图已保存到 {save_path}")

if __name__ == "__main__":
    create_static_charts()