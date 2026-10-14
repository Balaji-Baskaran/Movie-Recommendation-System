import plotly.graph_objects as go
import numpy as np

def make_heartbeat_chart(recs, query_title):
    IND_COLOR = {
        "Kollywood": "#fbbf24",
        "Bollywood": "#f87171",
        "Tollywood": "#4ade80",
        "Mollywood": "#38bdf8",
        "Sandalwood": "#c084fc",
    }
    def ind_col(ind): return IND_COLOR.get(ind, "#818cf8")

    def h2r(h, a=1.0):
        h = h.lstrip('#')
        r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
        return f"rgba({r},{g},{b},{a})"

    scores_pct = [rec["score"] * 100 for rec in recs]
    s_max  = max(scores_pct) if scores_pct else 100.0
    s_min  = min(scores_pct) if scores_pct else 0.0
    s_rng  = (s_max - s_min) or 1.0
    s_avg  = sum(scores_pct) / len(scores_pct) if scores_pct else 0

    def amp(raw):
        t = (raw - s_min) / s_rng
        return 5.0 + t * 95.0

    amp_scores = [amp(s) for s in scores_pct]

    def beat_points(i, a_h):
        p_h = a_h * 0.055
        q_h = -a_h * 0.065
        s_h = -a_h
        t_h = a_h  * 0.090

        x0 = i - 0.50
        return [
            (x0 + 0.00,  0.0), (x0 + 0.10,  0.0), (x0 + 0.16,  p_h),
            (x0 + 0.22,  0.0), (x0 + 0.28,  0.0), (x0 + 0.33,  q_h),
            (i,           a_h), (x0 + 0.62,  s_h), (x0 + 0.68,  0.0),
            (x0 + 0.75,  t_h), (x0 + 0.88,  0.0), (x0 + 1.00,  0.0),
        ]

    cx, cy = [], []
    for i, (rec, a_h, raw) in enumerate(zip(recs, amp_scores, scores_pct)):
        pts = beat_points(i, a_h)
        cx.extend(p[0] for p in pts)
        cy.extend(p[1] for p in pts)

    fig = go.Figure()

    for band in range(0, 120, 8):
        fig.add_hrect(y0=band, y1=band + 4, fillcolor='rgba(255,255,255,0.007)', line_width=0)

    for i, (rec, a_h, raw) in enumerate(zip(recs, amp_scores, scores_pct)):
        col   = ind_col(rec['industry'])
        tri_x = [i - 0.17, i, i + 0.12, i - 0.17]
        tri_y = [-a_h * 0.065, a_h, -a_h, -a_h * 0.065]
        fig.add_trace(go.Scatter(
            x=tri_x, y=tri_y, mode='lines', line=dict(color='rgba(0,0,0,0)', width=0),
            fill='toself', fillcolor=h2r(col, 0.13), hoverinfo='skip', showlegend=False,
        ))

    fig.add_trace(go.Scatter(
        x=cx, y=cy, mode='lines', line=dict(color='rgba(0,255,196,0.06)', width=14, shape='spline', smoothing=0.4),
        hoverinfo='skip', showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=cx, y=cy, mode='lines', line=dict(color='rgba(0,255,196,0.18)', width=6, shape='spline', smoothing=0.4),
        hoverinfo='skip', showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=cx, y=cy, mode='lines', line=dict(color='rgba(0,255,196,0.95)', width=1.7, shape='spline', smoothing=0.4),
        hoverinfo='skip', showlegend=False,
    ))

    for i, (rec, a_h, raw) in enumerate(zip(recs, amp_scores, scores_pct)):
        col = ind_col(rec['industry'])
        col_dim = h2r(col, 0.28)

        fig.add_shape(type='line', x0=i, x1=i, y0=-3, y1=a_h, line=dict(color=col_dim, width=1, dash='dot'))

        fig.add_trace(go.Scatter(
            x=[i], y=[a_h], mode='markers',
            marker=dict(color=col, size=16, opacity=0, symbol='circle'),
            hovertemplate=(
                f"<b>{rec['title']}</b>"
                f"<br><span style='color:{col}'>●</span> {rec['industry']}  ·  #{rec['rank']}"
                f"<br>Similarity  <b>{raw:.2f}%</b>"
                f"<br>Rating {rec['rating']}★  ·  {rec['year']}<extra></extra>"
            ), showlegend=False,
        ))

        fig.add_trace(go.Scatter(
            x=[i], y=[a_h], mode='markers',
            marker=dict(color=col, size=9, line=dict(color='rgba(255,255,255,0.7)', width=1.2), symbol='circle', opacity=1),
            hoverinfo='skip', showlegend=False,
        ))

        fig.add_annotation(
            x=i, y=a_h, text=f"<span style='font-family:Outfit;font-weight:700;font-size:10px;color:{col}'>{raw:.1f}%</span>",
            showarrow=False, yshift=17, xanchor='center',
        )

        fig.add_annotation(
            x=i, y=0, text=f"<span style='font-family:Outfit;font-size:9px;color:{col}'>#{rec['rank']}</span>",
            showarrow=False, yshift=-16, xanchor='center',
        )

    fig.add_hline(y=0, line=dict(color='rgba(239,68,68,0.35)', width=1))

    hud_best = f"BEST  {s_max:.1f}%"
    hud_avg  = f"AVG  {s_avg:.1f}%"
    hud_low  = f"WEAK  {s_min:.1f}%"
    for xpos, txt, col in [(0.01, hud_best, "#00ffc4"), (0.50, hud_avg, "#a78bfa"), (0.99, hud_low, "#fb923c")]:
        fig.add_annotation(
            text=f"<span style='font-family:\"Outfit\",monospace;font-size:10px;font-weight:700;letter-spacing:1px;color:{col}'>{txt}</span>",
            x=xpos, y=1.055, xref='paper', yref='paper', showarrow=False, xanchor='center',
        )

    present = list(dict.fromkeys(rec['industry'] for rec in recs))
    leg = "  ".join(f"<span style='color:{ind_col(ind)}'><b>●</b> {ind}</span>" for ind in present)
    fig.add_annotation(text=f"<span style='font-family:Inter;font-size:9.5px'>{leg}</span>", x=0.5, y=-0.26, xref='paper', yref='paper', showarrow=False, xanchor='center')

    tick_labels = [(rec['title'][:16] + '…' if len(rec['title']) > 16 else rec['title']) for rec in recs]
    n = len(recs)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(3, 5, 16, 0.88)',
        font=dict(family='Inter', color='rgba(203,213,225,0.85)'),
        title=dict(
            text=(
                '<span style="font-family:Outfit;font-weight:900;font-size:14px;letter-spacing:1px;color:rgba(203,213,225,0.9)">SIMILARITY PULSE</span>'
                f'<span style="font-family:Inter;font-size:11px;color:rgba(148,163,184,0.55)">  ·  {n} matches for  </span>'
                f'<span style="font-family:Outfit;font-weight:700;font-size:13px;color:#00ffc4">{query_title}</span>'
            ),
            x=0.01, xanchor='left', y=0.965,
        ),
        margin=dict(l=52, r=28, t=70, b=120), height=460, hovermode='closest',
        xaxis=dict(
            showgrid=True, gridcolor='rgba(239,68,68,0.13)', gridwidth=1,
            minor=dict(showgrid=True, gridcolor='rgba(239,68,68,0.04)', dtick=0.2),
            zeroline=False, tickmode='array', tickvals=list(range(n)), ticktext=tick_labels, tickangle=-45,
            tickfont=dict(size=9, family='Inter', color='rgba(203,213,225,0.65)'), range=[-0.55, n - 0.45],
        ),
        yaxis=dict(
            showgrid=True, gridcolor='rgba(239,68,68,0.10)', gridwidth=1,
            minor=dict(showgrid=True, gridcolor='rgba(239,68,68,0.03)', dtick=5),
            zeroline=False, tickfont=dict(size=9, color='rgba(148,163,184,0.40)'),
            title=dict(text='Match strength ▲', font=dict(size=9, family='Inter', color='rgba(148,163,184,0.35)')),
            range=[-110, 120], tickvals=[-95, -47, 0, 22, 47, 71, 95],
            ticktext=['-Top', '-Med', '─', 'Low', 'Med', 'High', 'Top'],
        ),
    )
    return fig
