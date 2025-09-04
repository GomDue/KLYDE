import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import MaxNLocator
from wordcloud import WordCloud


PALETTE = {
    "primary":   "#4C78A8",
    "accent":    "#F58518",
    "success":   "#54A24B",
    "warning":   "#E45756",
    "muted":     "#9EA3AC",
    "ink":       "#2F2F33",
    "grid":      "#E8EAED",
    "bg":        "#FFFFFF",
}

def _apply_base_style(ax, font_prop=None, with_grid=True):
    # 배경/스파인/그리드
    ax.set_facecolor(PALETTE["bg"])
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#D0D3D8")
    ax.spines["bottom"].set_color("#D0D3D8")
    if with_grid:
        ax.grid(axis="y", color=PALETTE["grid"], linewidth=1, alpha=0.7)
    # 폰트
    if font_prop is not None:
        ax.title.set_fontproperties(font_prop)
        ax.xaxis.label.set_fontproperties(font_prop)
        ax.yaxis.label.set_fontproperties(font_prop)
        for tick in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
            tick.set_fontproperties(font_prop)

def _annotate_bar_value(ax, rect, text, font_prop=None, offset=3):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + offset,
            text, ha="center", va="bottom", fontproperties=font_prop)

def _annotate_barh_value(ax, rect, text, font_prop=None, offset=3):
    width = rect.get_width()
    ax.text(width + offset, rect.get_y() + rect.get_height()/2,
            text, ha="left", va="center", fontproperties=font_prop)

def _format_dod(dod):
    if isinstance(dod, (int, float)):
        return f"{dod:+.1f}%"
    return str(dod)


def plot_kpi(sum_row, kw_rows, dod, title, font_prop):
    total = int(sum_row["total_articles"])
    uniq  = int(sum_row["unique_categories"])
    dod_s = _format_dod(dod)
    top_kw_text = "-"
    if kw_rows:
        top_kw = kw_rows[0]
        top_kw_text = f"{top_kw['keyword']} ({int(top_kw['count'])})"

    fig, ax = plt.subplots(figsize=(11.69, 3.7))  # A4 가로 비율에 맞춤
    ax.axis("off")
    fig.patch.set_facecolor(PALETTE["bg"])

    # 카드 배경
    card = FancyBboxPatch(
        (0.01, 0.05), 0.98, 0.9,
        boxstyle="round,pad=0.015,rounding_size=12",
        linewidth=1, edgecolor="#D6DAE0", facecolor="#FAFBFC", transform=ax.transAxes
    )
    ax.add_patch(card)

    # 헤더 바
    header = FancyBboxPatch(
        (0.01, 0.84), 0.98, 0.11,
        boxstyle="round,pad=0.01,rounding_size=12",
        linewidth=0, edgecolor="none", facecolor=PALETTE["primary"], transform=ax.transAxes
    )
    ax.add_patch(header)
    ax.text(0.03, 0.895, f"데일리 KPI  |  기준일: {title}",
            color="white", fontsize=18, fontproperties=font_prop, transform=ax.transAxes)

    # 4열 메트릭
    metrics = [
        ("기사 수", f"{total:,}  (DoD {dod_s})"),
        ("카테고리", f"{uniq:,}"),
        ("Top 키워드", top_kw_text),
        ("생성일", str(title)),
    ]
    x0, y0 = 0.03, 0.17
    gap_x = 0.24
    for i, (k, v) in enumerate(metrics):
        x = x0 + i * gap_x
        # 키
        ax.text(x, y0+0.15, k, color=PALETTE["muted"], fontsize=13,
                fontproperties=font_prop, transform=ax.transAxes)
        # 값
        ax.text(x, y0+0.03, v, color=PALETTE["ink"], fontsize=20,
                fontproperties=font_prop, transform=ax.transAxes)

    fig.tight_layout()
    return fig


def plot_trend(trend_pdf, sum_row, yester_date_str, font_prop):
    dates = trend_pdf["report_date"].astype(str).tolist() if not trend_pdf.empty else [yester_date_str]
    counts = trend_pdf["total_articles"].astype(int).tolist() if not trend_pdf.empty else [int(sum_row["total_articles"])]

    # 범주형 문자열 대신 숫자 인덱스로 그리기
    x = np.arange(len(dates))

    fig, ax = plt.subplots(figsize=(11.69, 3.7))
    _apply_base_style(ax, font_prop, with_grid=True)

    # 라인 + 마커 + 영역
    ax.plot(x, counts, marker="o", linewidth=2.5, markersize=6, color=PALETTE["primary"])
    ax.fill_between(x, counts, alpha=0.08, color=PALETTE["primary"])

    # 마지막 포인트 강조 (텍스트는 약간 오른쪽으로)
    ax.scatter([x[-1]], [counts[-1]], s=80, color=PALETTE["accent"], zorder=3)
    ax.text(x[-1] + 0.15, counts[-1], f" {counts[-1]:,}", va="center",
            color=PALETTE["accent"], fontproperties=font_prop)

    # 좌우 여백 주기
    ax.set_xlim(-0.6, len(x) - 0.4)

    # x축 눈금/라벨 다시 매핑
    ax.set_xticks(x)
    ax.set_xticklabels(dates, rotation=30)

    ax.set_title(f"{yester_date_str} 최근 기사 수 추이", fontproperties=font_prop, fontsize=16)
    ax.set_xlabel("날짜", fontproperties=font_prop)
    ax.set_ylabel("기사 수", fontproperties=font_prop)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    fig.tight_layout()
    return fig


def plot_hourly_bar(hours, counts, title, font_prop):
    fig, ax = plt.subplots(figsize=(11.69, 3.7))
    _apply_base_style(ax, font_prop, with_grid=True)

    bars = ax.bar(hours, counts, width=0.8, color=PALETTE["primary"], alpha=0.9)
    if counts:
        max_idx = int(np.argmax(counts))
        bars[max_idx].set_color(PALETTE["accent"])

    ax.set_xticks(range(0, 24, 1))
    ax.set_title(f"{title} 시간대 기사 분포", fontproperties=font_prop, fontsize=16)
    ax.set_xlabel("시", fontproperties=font_prop)
    ax.set_ylabel("기사 수", fontproperties=font_prop)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    for b, c in zip(bars, counts):
        if c > 0:
            _annotate_bar_value(ax, b, f"{c}", font_prop, offset=0.6)

    fig.tight_layout()
    return fig


def plot_keyword_counts(rows, title_str, font_prop, topn=10):
    if not rows:
        fig, ax = plt.subplots(figsize=(10, 6))
        _apply_base_style(ax, font_prop)
        ax.text(0.5, 0.5, "표시할 키워드가 없습니다.", ha="center", va="center",
                fontproperties=font_prop, fontsize=14)
        ax.axis("off")
        fig.tight_layout()
        return fig

    # 상위 N 정렬
    sorted_rows = sorted(rows, key=lambda r: int(r["count"]), reverse=True)[:topn]
    keywords = [r["keyword"] for r in sorted_rows][::-1]
    counts   = [int(r["count"]) for r in sorted_rows][::-1]

    # ---- 여백/크기 조정 ----
    # 가장 긴 키워드 길이에 따라 왼쪽 마진 가변 (0~1 비율)
    max_label_len = max((len(k) for k in keywords), default=5)
    left_margin = min(0.42, 0.12 + 0.012 * max_label_len)  # 기본 0.12 + 글자수 비례, 최대 0.42
    right_margin = 0.96  # 오른쪽은 값 라벨 공간 고려해 살짝만 여유

    fig, ax = plt.subplots(figsize=(11.69, 6.2))  # 가로폭을 넉넉히
    fig.subplots_adjust(left=left_margin, right=right_margin)
    _apply_base_style(ax, font_prop, with_grid=True)

    bars = ax.barh(keywords, counts, color=PALETTE["primary"], alpha=0.9)

    # 상위 1위 강조
    if bars:
        bars[-1].set_color(PALETTE["accent"])

    # x축 범위: 최대값의 15% 여유 (값 라벨이 잘리지 않도록)
    if counts:
        xmax = max(counts)
        ax.set_xlim(0, xmax * 1.15 + 1)
        value_offset = max(2, xmax * 0.015)  # 데이터 단위 기준 가변 오프셋
    else:
        value_offset = 3

    # 값 라벨
    for b, c in zip(bars, counts):
        _annotate_barh_value(ax, b, f"{c}", font_prop, offset=value_offset)

    ax.set_title(f"{title_str} News Keywords TOP {len(keywords)}",
                 fontproperties=font_prop, fontsize=16)
    ax.set_xlabel("Frequency", fontproperties=font_prop)
    ax.set_ylabel("Keywords", fontproperties=font_prop)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    fig.tight_layout()  # 내부 요소 정리 (subplots_adjust로 바깥 여백은 이미 확보함)
    return fig



def plot_category_counts(rows, title_str, font_prop, topn=10):
    if not rows:
        fig, ax = plt.subplots(figsize=(10, 6))
        _apply_base_style(ax, font_prop)
        ax.text(0.5, 0.5, "표시할 카테고리가 없습니다.", ha="center", va="center",
                fontproperties=font_prop, fontsize=14)
        ax.axis("off")
        fig.tight_layout()
        return fig

    sorted_rows = sorted(rows, key=lambda r: int(r["count"]), reverse=True)[:topn]
    cats   = [r["category"] for r in sorted_rows][::-1]
    counts = [int(r["count"]) for r in sorted_rows][::-1]

    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    _apply_base_style(ax, font_prop, with_grid=True)

    bars = ax.barh(cats, counts, color=PALETTE["primary"], alpha=0.9)
    if bars:
        bars[-1].set_color(PALETTE["accent"])

    for b, c in zip(bars, counts):
        _annotate_barh_value(ax, b, f"{c}", font_prop, offset=6)

    ax.set_title(f"{title_str} Top Categories (by Articles)", fontproperties=font_prop, fontsize=16)
    ax.set_xlabel("Frequency", fontproperties=font_prop)
    ax.set_ylabel("Category", fontproperties=font_prop)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    fig.tight_layout()
    return fig


def _wc_color_func(*args, **kwargs):
    # 통일된 팔레트 기반 리컬러 (primary~accent 사이 톤 랜덤)
    colors = [PALETTE["primary"], PALETTE["accent"], PALETTE["success"]]
    return np.random.choice(colors)

def plot_wordcloud(rows, title_str, font_path):
    freqs = {r["keyword"]: int(r["count"]) for r in rows if r.get("keyword") and int(r.get("count", 0)) > 0}

    fig, ax = plt.subplots(figsize=(12.5, 8.2))
    fig.patch.set_facecolor(PALETTE["bg"])
    if not freqs:
        ax.text(0.5, 0.5, "No keywords to plot",
                ha="center", va="center", fontsize=16)
        ax.set_title(f"{title_str} Word Cloud", fontsize=16)
        ax.axis("off")
        fig.tight_layout()
        return fig

    # 크기/해상도/배경/충돌방지 최적화
    wc = WordCloud(
        font_path=font_path,
        width=1800, height=1100,
        background_color="white",
        prefer_horizontal=0.95,
        collocations=False,
        max_words=300,
        relative_scaling=0.3,
        min_font_size=10,
        max_font_size=220,
        margin=4,
    ).generate_from_frequencies(freqs)

    wc = wc.recolor(color_func=_wc_color_func, random_state=37)

    ax.imshow(wc, interpolation="bilinear")
    ax.set_title(f"{title_str} Word Cloud", fontsize=16)
    ax.axis("off")
    fig.tight_layout()
    return fig


def save_pdf(report_path, figs):
    with PdfPages(report_path) as pdf:
        # PDF 메타데이터
        metadata = {
            "Title":  "Daily News Report",
            "Author": "KLYDE Pipeline",
            "Subject": "Daily KPIs, Trends, and Keyword Insights",
            "Keywords": "news, kpi, trend, keywords, categories, report"
        }
        pdf.infodict().update(metadata)
        for fig in figs:
            pdf.savefig(fig, bbox_inches="tight", dpi=300)
            plt.close(fig)
