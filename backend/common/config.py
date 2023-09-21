# Claudeに渡すパラメータの設定をします。
# ご利用のアプリケーションに合わせて調整してください。
# 参考: https://docs.anthropic.com/claude/reference/complete_post
GENERATION_CONFIG = {
    "maxTokenCount": 512,
    "temperature": 0,
    "topP": 0.9,
    "stopSequences": []
}
