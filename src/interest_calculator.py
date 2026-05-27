"""
信用卡还款利息估算函数
"""

def min_payment_interest(principal, daily_rate, monthly_payment_ratio=0.1, max_months=12):
    """
    最低还款利息估算（复利模型）
    每月先按日计息加入本金，再还固定比例，剩余本金进入下月。
    """
    balance = principal
    total_interest = 0.0
    days_per_month = 30

    for _ in range(max_months):
        if balance <= 1e-3:
            break
        interest = balance * daily_rate * days_per_month
        total_interest += interest
        balance += interest               # 利息资本化
        payment = balance * monthly_payment_ratio
        balance -= payment
        if balance < 0:
            balance = 0.0
    return round(total_interest, 2)



def installment_interest(principal, monthly_fee_rate, periods):
    """等额分期手续费（按期收取）"""
    total_fee = principal * monthly_fee_rate * periods
    return round(total_fee, 2)


def full_payment_interest():
    return 0.0


def annual_percentage_rate_from_monthly_fee(monthly_fee_rate, periods):
    """
    根据分期费率估算实际年化利率（近似IRR）
    仅用于展示，说明费率≠利率。
    """
    return round(monthly_fee_rate * 12 * 1.9 * 100, 2)
