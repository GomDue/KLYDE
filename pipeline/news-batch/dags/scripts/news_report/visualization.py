import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from wordcloud import WordCloud


def plot_kpi(sum_row, kw_rows, dod, title, font_prop):
    total = int(sum_row["total_articles"])
    uniq = int(sum_row["unique_categories"])
    if isinstance(dod, (int, float)):
        dod = f"{dod:+.1f}%"

    top_kw_text = "-"
    if kw_rows:
        top_kw_text = f"{kw_rows[0]['keyword']} ({kw_rows[0]['count']})"

    lines = [
        f"기준일: {title}",
        f"기사 수: {total:,} (DoD {dod})",
        f"카테고리: {uniq:,}",
        f"Top 키워드: {top_kw_text}",
    ]

    fig, ax = plt.subplots(figsize=(11, 4))
    ax.text(0.02, 0.70, lines[0], fontproperties=font_prop, fontsize=16)
    ax.text(0.02, 0.40, lines[1], fontproperties=font_prop, fontsize=16)
    ax.text(0.50, 0.70, lines[2], fontproperties=font_prop, fontsize=16)
    ax.text(0.50, 0.40, lines[3], fontproperties=font_prop, fontsize=16)
    fig.tight_layout()
    return fig

def plot_trend(trend_pdf, sum_row, yester_date_str, font_prop):
    dates = trend_pdf["report_date"].astype(str).tolist() if not trend_pdf.empty else [yester_date_str]
    counts = trend_pdf["total_articles"].astype(int).tolist() if not trend_pdf.empty else [int(sum_row["total_articles"])]

    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(dates, counts, marker="o")
    ax.set_title(f"{yester_date_str} 최근 추이", fontproperties=font_prop)
    ax.set_xlabel("날짜", fontproperties=font_prop)
    ax.set_ylabel("기사 수", fontproperties=font_prop)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig

def fig_hourly_bar(hours, counts, title, font_prop):
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.bar(hours, counts)

    ax.set_xticks(range(0, 24, 1))
    ax.set_title(f"{title} 시간대 기사 분포", fontproperties=font_prop)
    ax.set_xlabel("시", fontproperties=font_prop)
    ax.set_ylabel("기사 수", fontproperties=font_prop)
    fig.tight_layout()
    return fig

def plot_keyword_counts(rows, title_str, font_prop):
    keywords = [r["keyword"] for r in rows]
    counts = [r["count"] for r in rows]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(keywords[::-1], counts[::-1], label="Keywords")
    for bar, count in zip(bars, counts[::-1]):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.2, str(count),
                ha="center", va="bottom", fontproperties=font_prop)
    
    ax.set_title(f"{title_str} News Keywords TOP 10", fontproperties=font_prop)
    ax.set_xlabel("Keywords", fontproperties=font_prop)
    ax.set_ylabel("Frequency", fontproperties=font_prop)
    ax.tick_params(axis="x", rotation=45, labelsize=10)
    ax.tick_params(axis="y", labelsize=10)
    ax.axhline(y=0, linewidth=1)
    return fig

def plot_category_counts(rows, title_str, font_prop):
    cats   = [r["category"] for r in rows]
    counts = [r["count"] for r in rows]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(cats[::-1], counts[::-1], label="Categories")
    for bar, count in zip(bars, counts[::-1]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2, str(count),
                ha="left", va="center", fontproperties=font_prop)
        
    ax.set_title(f"{title_str} Top Categories (by Articles)", fontproperties=font_prop)
    ax.set_xlabel("Frequency", fontproperties=font_prop)
    ax.set_ylabel("Category", fontproperties=font_prop)
    ax.tick_params(axis="y", rotation=0, labelsize=10)
    ax.tick_params(axis="x", labelsize=10)
    return fig

def plot_wordcloud(rows, title_str, font_path):
    freqs = {r["keyword"]: int(r["count"]) for r in rows if r.get("keyword")}

    if not freqs:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(
            0.5, 0.5,
            "No keywords to plot",
            ha="center", va="center", fontsize=16
        )
        ax.set_title(f"{title_str} Word Cloud", fontsize=16)
        ax.axis("off")
        fig.tight_layout()
        return fig
    
    wc = WordCloud(
        font_path=font_path, 
        width=1400, height=900,
        background_color="white",
        prefer_horizontal=0.9,
        collocations=False
    ).generate_from_frequencies(freqs)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wc, interpolation="bilinear")
    ax.set_title(f"{title_str} Word Cloud", fontsize=16)
    ax.axis("off")
    fig.tight_layout()
    return fig

def save_pdf(report_path, figs):
    with PdfPages(report_path) as pdf:
        for fig in figs:
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)
