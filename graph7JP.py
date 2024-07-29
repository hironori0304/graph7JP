import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import japanize_matplotlib

st.title('グラフ作成アプリ')

# グラフタイトル、x軸、y軸のタイトル入力
st.sidebar.header('グラフ設定')
graph_title = st.sidebar.text_input('グラフタイトル', '平均値と標準誤差の棒グラフ')
x_axis_title = st.sidebar.text_input('X軸タイトル', 'カテゴリー')
y_axis_title = st.sidebar.text_input('Y軸タイトル', '値')

# フォントサイズ設定
title_fontsize = st.sidebar.slider('タイトルフォントサイズ', min_value=10, max_value=30, value=20, step=1)
label_fontsize = st.sidebar.slider('ラベルフォントサイズ', min_value=10, max_value=20, value=14, step=1)
tick_fontsize = st.sidebar.slider('目盛りラベルフォントサイズ', min_value=8, max_value=20, value=12, step=1)
axis_num_fontsize = st.sidebar.slider('軸番号フォントサイズ', min_value=8, max_value=20, value=12, step=1)

# 線の太さ設定
linewidth = st.sidebar.slider('線の太さ', min_value=0.5, max_value=5.0, value=1.0, step=0.1)

# グループ数の入力
num_groups = st.sidebar.number_input('グループ数', min_value=1, max_value=10, value=3, step=1)

# グラフサイズの入力
width = st.sidebar.number_input('グラフの幅', min_value=4.0, max_value=20.0, value=8.0, step=0.5)
height = st.sidebar.number_input('グラフの高さ', min_value=3.0, max_value=15.0, value=6.0, step=0.5)

# 棒グラフの色選択
bar_color = st.sidebar.selectbox('棒グラフの色', options=['skyblue', 'lightgreen', 'salmon', 'gold', 'plum'])

# 平均値、標準誤差、グループ名、有意差の入力
means = []
std_errors = []
group_names = []
significance_pairs = []

for i in range(num_groups):
    group_name = st.sidebar.text_input(f'グループ名 (グループ {i+1})', f'グループ {i+1}', key=f'group_name_{i}')
    mean = st.sidebar.number_input(f'平均値 (グループ {i+1})', value=0.0, format='%f', key=f'mean_{i}')
    std_error = st.sidebar.number_input(f'標準誤差 (グループ {i+1})', value=0.0, format='%f', key=f'std_error_{i}')
    means.append(mean)
    std_errors.append(std_error)
    group_names.append(group_name)

for i in range(num_groups):
    for j in range(i + 1, num_groups):
        significant = st.sidebar.checkbox(f'グループ {i+1} とグループ {j+1} の間の有意差', key=f'significant_{i}_{j}')
        if significant:
            significance_pairs.append((i, j))

# グラフを作成
fig, ax = plt.subplots(figsize=(width, height))

x = np.arange(len(means))
error_bar_params = dict(capsize=5, linewidth=linewidth)  # エラーバーのパラメータ

bars = ax.bar(x, means, yerr=std_errors, capsize=5, color=bar_color, alpha=0.7, error_kw=error_bar_params)

# 棒に境界線を追加
for bar in bars:
    bar.set_edgecolor('black')
    bar.set_linewidth(linewidth)

ax.set_xlabel(x_axis_title, fontsize=label_fontsize)
ax.set_ylabel(y_axis_title, fontsize=label_fontsize)
ax.set_title(graph_title, fontsize=title_fontsize)
ax.set_xticks(x)
ax.set_xticklabels(group_names, fontsize=tick_fontsize)

# 軸の線の太さを設定
ax.spines['top'].set_linewidth(linewidth)
ax.spines['right'].set_linewidth(linewidth)
ax.spines['left'].set_linewidth(linewidth)
ax.spines['bottom'].set_linewidth(linewidth)

# y軸の目盛りラベルのフォントサイズを設定
ax.tick_params(axis='y', labelsize=axis_num_fontsize)

# 有意差の線とラベルを追加
line_spacing = max(std_errors) * 2  # 一定の間隔

# 最初と最後のグループ間の有意差の線を最上部に配置
significance_pairs = sorted(significance_pairs, key=lambda pair: (pair != (0, num_groups - 1), pair))

# 有意差の線の最高位置を追跡
max_y = max(means) + max(std_errors) + (len(significance_pairs) + 1) * line_spacing

for idx, (i, j) in enumerate(significance_pairs):
    x1, x2 = x[i], x[j]
    y = max_y - (idx + 1) * line_spacing
    h, col = 0.2, 'k'
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=linewidth, c=col)
    ax.text((x1 + x2) * 0.5, y + h, "p<0.05", ha='center', va='bottom', color=col, fontsize=tick_fontsize)

# グラフを表示
st.pyplot(fig)

# ダウンロードボタンを追加
buffer = BytesIO()
fig.savefig(buffer, format="png")
buffer.seek(0)

st.download_button(
    label="グラフをPNGとしてダウンロード",
    data=buffer,
    file_name="graph.png",
    mime="image/png"
)
