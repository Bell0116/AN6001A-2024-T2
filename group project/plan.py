from flask import Flask, render_template, request
import google.generativeai as genai

genai.configure(api_key="AIzaSyBRuD5dvIrCBTDllqGo5mOy_bg4uMBRA6M")
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# 主页
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("Index.html")

# 生成个性化饮食计划
@app.route("/meal_plan", methods=["POST"])
def meal_plan():
    goal = request.form.get("goal")  # 获取用户目标（增肌/减脂）
    preferences = request.form.get("preferences")  # 获取食材偏好

    # 构造提示词
    prompt = f"""
    My goal is: {goal}.
    My ingredient preferences are：{preferences}.
    Please provide a personalized diet plan that generates recommendations for three meals per day.
    """

    # 让 Gemini AI 生成饮食计划
    response = model.generate_content(prompt)

    # 解析 AI 生成的文本
    try:
        meal_plan_text = response.candidates[0].content.parts[0].text
    except:
        meal_plan_text = "无法生成饮食计划，请稍后重试。"

    return render_template("meal_plan.html", meal_plan=meal_plan_text)

if __name__ == "__main__":
    app.run(debug=True)
