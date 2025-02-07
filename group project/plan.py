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
    Please generate a diet plan similar to Mint Health that contains:
    1. total calories (kcal) and nutrient ratios (protein, fat, carbohydrates).
    2. detailed recommendations for three meals (food + grams).
    3. an option to change foods.

    The format is as follows:
    ``
    Total calories: 2200 kcal
    Nutritional ratio: Protein 30% (165g), Fat 20% (49g), Carbohydrate 50% (275g).

    Morning (450kcal).
    - Oatmeal 100g
    - 2 poached eggs
    - Soymilk without sugar 200ml

    Lunch (800kcal).
    - Black rice 150g
    - Grilled chicken breast 100g
    - Broccoli 50g

    Dinner (700kcal).
    - Sweet Potato 200g
    - Salmon 120g
    - Avocado 50g
    、、
    Please follow the format output strictly! And A few lines between each meal. And it should be daily plan with 7 days a week.
    """


    # 让 Gemini AI 生成饮食计划
    response = model.generate_content(prompt)

    # 解析 AI 生成的文本
    try:
        meal_plan_text = response.candidates[0].content.parts[0].text
    except:
        meal_plan_text = "Unable to generate diet plan, please try again later."

    return render_template("meal_plan.html", meal_plan=meal_plan_text)

if __name__ == "__main__":
    app.run(debug=True)
