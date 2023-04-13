import matplotlib.pyplot as plt

expenses = [35, 25, 20, 15, 10]
categories = ["Shopping", "Food", "Luxury", "Groceries", "Other"]

timeframe = ['Aug 2022', 'Sep 2022', 'Oct 2022', 'Nov 2020', 'Dec 2022']
total_expense = [2700.0, 2000.0, 1000.0, 400.0, 1500.0]


def get_shape(index, values):
    prev = index - 1
    next = index + 1
    n = len(values)

    peak = False
    valley = False
    slope = False
    hill = False

    if prev >= 0 and next < n:
        if values[index] > values[prev] and values[index] > values[next]:
            peak = True
        elif values[index] < values[prev] and values[index] < values[next]:
            valley = True
        elif values[index] > values[prev] and values[index] < values[next]:
            hill = True
        elif values[index] < values[prev] and values[index] > values[next]:
            slope = True
    return peak, valley, slope, hill

def create_pie_chart(expenses, categories):
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.title("Expense Trends", pad=20, fontdict={'fontsize': 18,'fontweight': 50 ,'color': 'purple', 'horizontalalignment': 'center'})
    patches, texts, pcts = ax.pie(expenses, labels=categories, startangle=90, autopct='%.1f%%',wedgeprops={'linewidth': 1.5, 'edgecolor': 'white'})
    ax.legend(categories, bbox_to_anchor=(1, 0, 0.5, 1), loc="center left")
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.75)
    for i, patch in enumerate(patches):
        texts[i].set_color(patch.get_facecolor())
    plt.setp(pcts, color='white', fontweight='bold')
    plt.setp(texts, fontweight=600)
    plt.show() 



def create_bar_chart(expenses, categories): 
    fig, ax = plt.subplots()
    colors = ['#EC7063', '#ABEBC6', '#F9E79F', '#D2B4DE', '#F0B27A', '#76D7C4', '#F5B7B1', '#5DADE2', '#17A589', '#F7DC6F', '#A569BD']
    bars = ax.bar(
        x=categories,
        height=expenses,
        color=colors
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)

    for i, bar in enumerate(bars):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            round(bar.get_height(), 1),
            horizontalalignment='center',
            color='black',
            weight='bold'
        )

    ax.set_xlabel('Expense Categories', labelpad=15, color='#333333')
    ax.set_ylabel('Amount Spended', labelpad=15, color='#333333')
    ax.set_title('Category wise expense trends', pad=15, color='blue', weight='bold')
    fig.tight_layout()
    plt.show()
    

def create_line_chart(total_expense, timeframe):
    fig, ax = plt.subplots()
    
    ax.plot(timeframe, total_expense, lw=2)
    ax.scatter(timeframe, total_expense, fc="red", s=50, lw=1.5, ec="white", zorder=12)

    for i, v in enumerate(total_expense):
        x_pad = 10
        y_pad = 20
        peak, valley, slope, hill = get_shape(i, total_expense)
        if peak:
            y_pad = 20
        if valley:
            y_pad = 20
        if slope:
            y_pad = 20
        if hill:
            y_pad = 20
        ax.annotate(str(v), xy=(i,v), xytext=(x_pad, y_pad), textcoords='offset points', ha="center")
    ax.set_xlabel('Time Duration', labelpad=5, color='#333333')
    ax.set_ylabel('Amount Spended', labelpad=5, color='#333333')
    ax.set_title('Duration wise expense trends', pad=10, color='blue', weight='bold')
    # plt.subplots_adjust(left=2, right=10)
    # plt.tight_layout(pad=0.9)

    plt.show()

# create_pie_chart(expenses, categories)
# create_bar_chart(expenses, categories)

create_line_chart(total_expense, timeframe)

