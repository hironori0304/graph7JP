import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import japanize_matplotlib
from io import BytesIO

st.title('Graph Creation App')

# Graph title, x-axis, and y-axis titles input
st.sidebar.header('Graph Settings')
graph_title = st.sidebar.text_input('Graph Title', '平均と標準誤差を含む棒グラフ')
x_axis_title = st.sidebar.text_input('X-axis Title', 'カテゴリ')
y_axis_title = st.sidebar.text_input('Y-axis Title', '値')

# Font size settings
title_fontsize = st.sidebar.slider('Title Font Size', min_value=10, max_value=30, value=20, step=1)
label_fontsize = st.sidebar.slider('Label Font Size', min_value=10, max_value=20, value=14, step=1)
tick_fontsize = st.sidebar.slider('Tick Label Font Size', min_value=8, max_value=20, value=12, step=1)
axis_num_fontsize = st.sidebar.slider('Axis Number Font Size', min_value=8, max_value=20, value=12, step=1)

# Line width setting
linewidth = st.sidebar.slider('Line Width', min_value=0.5, max_value=5.0, value=1.0, step=0.1)

# Number of groups input
num_groups = st.sidebar.number_input('Number of Groups', min_value=1, max_value=10, value=3, step=1)

# Graph size input
width = st.sidebar.number_input('Graph Width', min_value=4.0, max_value=20.0, value=8.0, step=0.5)
height = st.sidebar.number_input('Graph Height', min_value=3.0, max_value=15.0, value=6.0, step=0.5)

# Bar color selection
bar_color = st.sidebar.selectbox('Bar Color', options=['skyblue', 'lightgreen', 'salmon', 'gold', 'plum'])

# Means, standard errors, group names, and significance input
means = []
std_errors = []
group_names = []
significance_pairs = []

for i in range(num_groups):
    group_name = st.sidebar.text_input(f'Group Name (Group {i+1})', f'Group {i+1}', key=f'group_name_{i}')
    mean = st.sidebar.number_input(f'Mean (Group {i+1})', value=0.0, format='%f', key=f'mean_{i}')
    std_error = st.sidebar.number_input(f'Standard Error (Group {i+1})', value=0.0, format='%f', key=f'std_error_{i}')
    means.append(mean)
    std_errors.append(std_error)
    group_names.append(group_name)

for i in range(num_groups):
    for j in range(i + 1, num_groups):
        significant = st.sidebar.checkbox(f'Significant difference between Group {i+1} and Group {j+1}', key=f'significant_{i}_{j}')
        if significant:
            significance_pairs.append((i, j))

# Create the graph
fig, ax = plt.subplots(figsize=(width, height))

x = np.arange(len(means))
error_bar_params = dict(capsize=5, linewidth=linewidth)  # Error bar params

bars = ax.bar(x, means, yerr=std_errors, capsize=5, color=bar_color, alpha=0.7, error_kw=error_bar_params)

# Add border to bars with uniform line width
for bar in bars:
    bar.set_edgecolor('black')
    bar.set_linewidth(linewidth)

ax.set_xlabel(x_axis_title, fontsize=label_fontsize)
ax.set_ylabel(y_axis_title, fontsize=label_fontsize)
ax.set_title(graph_title, fontsize=title_fontsize)
ax.set_xticks(x)
ax.set_xticklabels(group_names, fontsize=tick_fontsize)

# Set line width for axes
ax.spines['top'].set_linewidth(linewidth)
ax.spines['right'].set_linewidth(linewidth)
ax.spines['left'].set_linewidth(linewidth)
ax.spines['bottom'].set_linewidth(linewidth)

# Set y-axis numbers font size
ax.tick_params(axis='y', labelsize=axis_num_fontsize)

# Add significance lines and labels
line_spacing = max(std_errors) * 2  # Uniform line spacing

# Ensure the significance line between the first and last group is at the top
significance_pairs = sorted(significance_pairs, key=lambda pair: (pair != (0, num_groups - 1), pair))

# Track highest y-position for significance lines
max_y = max(means) + max(std_errors) + (len(significance_pairs) + 1) * line_spacing

for idx, (i, j) in enumerate(significance_pairs):
    x1, x2 = x[i], x[j]
    y = max_y - (idx + 1) * line_spacing
    h, col = 0.2, 'k'
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=linewidth, c=col)
    ax.text((x1 + x2) * 0.5, y + h, "p<0.05", ha='center', va='bottom', color=col, fontsize=tick_fontsize)

# Display the graph
st.pyplot(fig)

# Add download button
buffer = BytesIO()
fig.savefig(buffer, format="png")
buffer.seek(0)

st.download_button(
    label="Download Graph as PNG",
    data=buffer,
    file_name="graph.png",
    mime="image/png"
)
