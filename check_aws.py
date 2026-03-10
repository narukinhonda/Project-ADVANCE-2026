import boto3

def hello_aws():
    try:
        # AWSの「自分の身分」を確認する命令を送る
        sts = boto3.client('sts')
        response = sts.get_caller_identity()
        
        print("\n✅ AWSへの接続に成功しました！")
        print(f"提督のアカウントID: {response['Account']}")
        print(f"現在のユーザー: {response['Arn']}")
        
    except Exception as e:
        print("\n❌ 接続に失敗しました...")
        print(f"エラー内容: {e}")

if __name__ == "__main__":
    hello_aws()