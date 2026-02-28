import boto3
from datetime import datetime, timedelta

def get_aws_cost_jpy():
    client = boto3.client('ce')
    
    # 期間の設定
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    start_date = yesterday.strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')

    # 為替レート（仮に1ドル=150円とします。自動取得も可能ですがまずは固定で）
    exchange_rate = 150 

    try:
        response = client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='DAILY',
            Metrics=['UnblendedCost']
        )

        for result in response['ResultsByTime']:
            usd_amount = float(result['Total']['UnblendedCost']['Amount'])
            jpy_amount = usd_amount * exchange_rate # ここで円換算
            
            print(f"\n📅 日付: {start_date}")
            print(f"💵 コスト (USD): ${usd_amount:.2f}")
            print(f"💴 コスト (JPY): ￥{int(jpy_amount)} （1ドル={exchange_rate}円計算）")

    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    get_aws_cost_jpy()