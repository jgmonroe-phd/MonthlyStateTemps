import pandas as pd
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import time

data = pd.read_csv('MonthlyAvgs.csv')
data.set_index(['State'], inplace=True)
data.sort_values('Annual')
data = data.T
annual_indx = data.index.isin(['Annual'])
# data.drop('Annual', axis=0, inplace=True)

# Setup figure
plt.ion()
fig, ax = plt.subplots(figsize=(6, 5))
ax.set_ylim([0, 94])

# Use month names for x-axis and label y-axis
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
x_labels = list(data.index[1:])
plt.xticks(x, x_labels, fontname='serif')
plt.ylabel('Temp (F)', fontname='serif')
plt.yticks([10*i for i in range(10)], fontname='serif')
# plt.grid()

# Set fonts: see http://matplotlib.org/api/font_manager_api.html#matplotlib.font_manager.FontProperties
bold_font = FontProperties()
bold_font.set_size('large')
bold_font.set_weight('bold')
bold_font.set_family('serif')
normal_font = FontProperties()
normal_font.set_family('serif')

file_path = 'C:\\Users\\'

# Make figure. from https://github.com/matplotlib/matplotlib/issues/7759/
lines = {}  # See https://matplotlib.org/api/lines_api.html
i = 0
k = 0
for state in data:
    # Recolor all lines to gray
    [l.set_color('0.8') for l in ax.lines]

    # Plot avg monthly temperatures (not annual avg) as green line (see http://matplotlib.org/users/colors.html)
    # Also, saves line objects to dictionary with state names as keys
    # If line will be highlighted later, set z-order very high to keep to front
    if state in ['Florida', 'NorthDakota']:
        lines[state] = ax.plot(x, data[~annual_indx][state], 'k', label=state, zorder=(50+i))
        i += 1
    else:
        lines[state] = ax.plot(x, data[~annual_indx][state], 'k', label=state, zorder=i)
        i += 1

    # Add text: see https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.figtext
    state_name = plt.figtext(0.15, 0.8, state, backgroundcolor='w', fontproperties=bold_font)
    avg_text = 'Avg Temp = ' + str(data[state]['Annual']) + 'F'
    avg_temp = plt.figtext(0.15, 0.755, avg_text, backgroundcolor='w', fontproperties=normal_font)

    # Display figure
    fig.canvas.flush_events()
    # print state, k
    k += 1
	# Turn on sleep and comment out save fig to view in realtime
    # time.sleep(0.25)
    fig_name = str(k) + '_' + state + '.png'
    fig.savefig(file_path+fig_name, dpi=200, bbox_inches='tight')

    # Remove old text
    state_name.set_visible(False)
    avg_temp.set_visible(False)

# Min/max/StDev (all calculated in external spreadsheet)
min_text = 'North Dakota: lowest avg annual temp (' + str(data['NorthDakota']['Annual']) + 'F)' + \
           '\n                        & most temp variation (StDev=22.9F)'
plt.figtext(0.235, 0.14, min_text, backgroundcolor='w', color='b', fontproperties=normal_font)
lines['NorthDakota'][0].set_color('b')
lines['NorthDakota'][0].set_linewidth(3)

max_text = 'Florida: highest avg annual temp (' + str(data['Florida']['Annual']) + 'F)' + \
           '\n              & least temp variation (StDev=8.4F)'
plt.figtext(0.14, 0.81, max_text, backgroundcolor='w', color='r', fontproperties=normal_font)
lines['Florida'][0].set_color('r')
lines['Florida'][0].set_linewidth(3)

fig.savefig(file_path+'final.png', dpi=200, bbox_inches='tight')

plt.ioff()
plt.show()

# Test plot
# plt.plot(x, data[~annual_indx]['Mississippi'], label='Mississippi')
# plt.plot(x, data[~annual_indx]['Michigan'], label='Michigan')
