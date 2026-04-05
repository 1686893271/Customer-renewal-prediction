from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# 读取数据
df = pd.read_excel('assets/policy_data.xlsx')

# 读取预测数据
df_test = pd.read_excel('assets/policy_test_predictions.xlsx')

@app.route('/')
def index():
    # 直接返回index.html的内容
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/occupation')
def get_occupation():
    # 只返回职业分布数据
    return jsonify({
        'occupation_distribution': [
            {"occupation": "医生", "count": 267},
            {"occupation": "律师", "count": 266},
            {"occupation": "工程师", "count": 244},
            {"occupation": "设计师", "count": 78},
            {"occupation": "销售", "count": 73}
        ]
    })

@app.route('/data')
def get_data():
    # 准备数据

    
    # 逻辑回归系数数据
    logistic_coefficients = [
        {'feature': 'income_level', 'coefficient': -2.0707},
        {'feature': 'gender', 'coefficient': -0.6973},
        {'feature': 'education_level', 'coefficient': -0.4677},
        {'feature': 'occupation', 'coefficient': -0.4673},
        {'feature': 'marital_status', 'coefficient': -0.4358},
        {'feature': 'insurance_region', 'coefficient': -0.0444},
        {'feature': 'premium_amount', 'coefficient': 0.0000},
        {'feature': 'policy_term', 'coefficient': 0.0334},
        {'feature': 'birth_region', 'coefficient': 0.0461},
        {'feature': 'age', 'coefficient': 0.0880},
        {'feature': 'family_members', 'coefficient': 0.7484}
    ]
    
    # 决策树特征重要性数据
    decision_tree_importance = [
        {'feature': 'age', 'importance': 0.451067},
        {'feature': 'marital_status', 'importance': 0.220229},
        {'feature': 'family_members', 'importance': 0.094090},
        {'feature': 'occupation', 'importance': 0.074502},
        {'feature': 'education_level', 'importance': 0.039579},
        {'feature': 'gender', 'importance': 0.036809},
        {'feature': 'premium_amount', 'importance': 0.031590},
        {'feature': 'insurance_region', 'importance': 0.024159},
        {'feature': 'birth_region', 'importance': 0.019631},
        {'feature': 'policy_term', 'importance': 0.008345},
        {'feature': 'income_level', 'importance': 0.000000}
    ]
    
    # 新客户预测数据
    new_customer_analysis = {
        'total_customers': len(df_test),
        'predicted_renewal': len(df_test[df_test['predicted_renewal'] == 'Yes']),
        'predicted_not_renewal': len(df_test[df_test['predicted_renewal'] == 'No']),
        'renewal_rate': len(df_test[df_test['predicted_renewal'] == 'Yes']) / len(df_test) * 100,
        'age_analysis': [
            {'age_group': '20-30', 'renewal_rate': len(df_test[(df_test['age'] >= 20) & (df_test['age'] < 30) & (df_test['predicted_renewal'] == 'Yes')]) / len(df_test[(df_test['age'] >= 20) & (df_test['age'] < 30)]) * 100 if len(df_test[(df_test['age'] >= 20) & (df_test['age'] < 30)]) > 0 else 0},
            {'age_group': '30-40', 'renewal_rate': len(df_test[(df_test['age'] >= 30) & (df_test['age'] < 40) & (df_test['predicted_renewal'] == 'Yes')]) / len(df_test[(df_test['age'] >= 30) & (df_test['age'] < 40)]) * 100 if len(df_test[(df_test['age'] >= 30) & (df_test['age'] < 40)]) > 0 else 0},
            {'age_group': '40-50', 'renewal_rate': len(df_test[(df_test['age'] >= 40) & (df_test['age'] < 50) & (df_test['predicted_renewal'] == 'Yes')]) / len(df_test[(df_test['age'] >= 40) & (df_test['age'] < 50)]) * 100 if len(df_test[(df_test['age'] >= 40) & (df_test['age'] < 50)]) > 0 else 0},
            {'age_group': '50-60', 'renewal_rate': len(df_test[(df_test['age'] >= 50) & (df_test['age'] < 60) & (df_test['predicted_renewal'] == 'Yes')]) / len(df_test[(df_test['age'] >= 50) & (df_test['age'] < 60)]) * 100 if len(df_test[(df_test['age'] >= 50) & (df_test['age'] < 60)]) > 0 else 0},
            {'age_group': '60+', 'renewal_rate': len(df_test[(df_test['age'] >= 60) & (df_test['predicted_renewal'] == 'Yes')]) / len(df_test[df_test['age'] >= 60]) * 100 if len(df_test[df_test['age'] >= 60]) > 0 else 0}
        ],
        'marital_analysis': [
            {'status': '单身', 'renewal_rate': len(df_test[(df_test['marital_status'] == '单身') & (df_test['predicted_renewal'] == 'Yes')]) / len(df_test[df_test['marital_status'] == '单身']) * 100 if len(df_test[df_test['marital_status'] == '单身']) > 0 else 0},
            {'status': '已婚', 'renewal_rate': len(df_test[(df_test['marital_status'] == '已婚') & (df_test['predicted_renewal'] == 'Yes')]) / len(df_test[df_test['marital_status'] == '已婚']) * 100 if len(df_test[df_test['marital_status'] == '已婚']) > 0 else 0},
            {'status': '其他', 'renewal_rate': len(df_test[(df_test['marital_status'] != '单身') & (df_test['marital_status'] != '已婚') & (df_test['predicted_renewal'] == 'Yes')]) / len(df_test[(df_test['marital_status'] != '单身') & (df_test['marital_status'] != '已婚')]) * 100 if len(df_test[(df_test['marital_status'] != '单身') & (df_test['marital_status'] != '已婚')]) > 0 else 0}
        ],
        'income_analysis': [
            {'level': '低', 'renewal_rate': len(df_test[(df_test['income_level'] == '低') & (df_test['predicted_renewal'] == 'Yes')]) / len(df_test[df_test['income_level'] == '低']) * 100 if len(df_test[df_test['income_level'] == '低']) > 0 else 0},
            {'level': '中', 'renewal_rate': len(df_test[(df_test['income_level'] == '中') & (df_test['predicted_renewal'] == 'Yes')]) / len(df_test[df_test['income_level'] == '中']) * 100 if len(df_test[df_test['income_level'] == '中']) > 0 else 0},
            {'level': '高', 'renewal_rate': len(df_test[(df_test['income_level'] == '高') & (df_test['predicted_renewal'] == 'Yes')]) / len(df_test[df_test['income_level'] == '高']) * 100 if len(df_test[df_test['income_level'] == '高']) > 0 else 0}
        ]
    }
    
    data = {
        # 1. 年龄分布
        'age_distribution': [
            {'age': '20-30', 'count': len(df[(df['age'] >= 20) & (df['age'] < 30)])},
            {'age': '30-40', 'count': len(df[(df['age'] >= 30) & (df['age'] < 40)])},
            {'age': '40-50', 'count': len(df[(df['age'] >= 40) & (df['age'] < 50)])},
            {'age': '50-60', 'count': len(df[(df['age'] >= 50) & (df['age'] < 60)])},
            {'age': '60+', 'count': len(df[df['age'] >= 60])}
        ],
        # 2. 性别分布
        'gender_distribution': [
            {'gender': '男', 'count': len(df[df['gender'] == '男'])},
            {'gender': '女', 'count': len(df[df['gender'] == '女'])}
        ],
        # 3. 收入水平分布
        'income_distribution': [
            {'level': '低', 'count': len(df[df['income_level'] == '低'])},
            {'level': '中', 'count': len(df[df['income_level'] == '中'])},
            {'level': '高', 'count': len(df[df['income_level'] == '高'])}
        ],
        # 4. 职业分布（取前5个）
        'occupation_distribution': [
            {"occupation": "医生", "count": 267},
            {"occupation": "律师", "count": 266},
            {"occupation": "工程师", "count": 244},
            {"occupation": "设计师", "count": 78},
            {"occupation": "销售", "count": 73}
        ],
        # 5. 续保情况
        'renewal_distribution': [
            {'status': 'Yes', 'count': len(df[df['renewal'] == 'Yes'])},
            {'status': 'No', 'count': len(df[df['renewal'] == 'No'])}
        ],
        # 6. 逻辑回归系数
        'logistic_coefficients': logistic_coefficients,
        # 7. 决策树特征重要性
        'decision_tree_importance': decision_tree_importance,
        # 8. 新客户预测分析
        'new_customer_analysis': new_customer_analysis
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)