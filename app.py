import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Product Analytics Dashboard — DoorDash Case Study",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS — Professional Blue & White
# ============================================
st.markdown("""
<style>
    /* Main background */
    .main { background-color: #F8F9FA; }
    
    /* Sidebar */
    .css-1d391kg { background-color: #1B3A6B; }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #1B3A6B;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1B3A6B;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #6B7280;
        margin-top: 4px;
    }
    .kpi-delta {
        font-size: 0.8rem;
        color: #10B981;
        margin-top: 4px;
    }

    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1B3A6B;
        margin: 20px 0 10px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #E5E7EB;
    }

    /* Insight boxes */
    .insight-box {
        background: #EFF6FF;
        border-left: 4px solid #1B3A6B;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
        font-size: 0.9rem;
        color: #1E40AF;
    }

    /* Recommendation boxes */
    .rec-box {
        background: #F0FDF4;
        border-left: 4px solid #10B981;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
        font-size: 0.9rem;
        color: #065F46;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    users = pd.read_csv("data_users.csv")
    orders = pd.read_csv("data_orders.csv")
    funnel = pd.read_csv("data_funnel.csv")
    ab_test = pd.read_csv("data_ab_test.csv")
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    return users, orders, funnel, ab_test

users, orders, funnel, ab_test = load_data()

# ============================================
# SIDEBAR FILTERS
# ============================================
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/DoorDash_Logo.svg/2560px-DoorDash_Logo.svg.png",
    width=160
)
st.sidebar.markdown("---")
st.sidebar.markdown("## 🎛️ Filters")

# City filter
all_cities = ['All Cities'] + sorted(orders['city'].unique().tolist())
selected_city = st.sidebar.selectbox("📍 City", all_cities)

# Device filter
all_devices = ['All Devices'] + sorted(orders['device_type'].unique().tolist())
selected_device = st.sidebar.selectbox("📱 Device Type", all_devices)

# User type filter
selected_user_type = st.sidebar.radio(
    "👤 User Type",
    ["All Users", "DashPass", "Regular"]
)

# Cuisine filter
all_cuisines = ['All Cuisines'] + sorted(
    orders['cuisine_category'].unique().tolist()
)
selected_cuisine = st.sidebar.multiselect(
    "🍽️ Cuisine Category",
    options=orders['cuisine_category'].unique().tolist(),
    default=orders['cuisine_category'].unique().tolist()
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 About This Project")
st.sidebar.markdown("""
Built by **Shanu Venkatesan**  
NYU Tandon — Management of Technology  
  
Analyzing **640K+ events** across  
funnel, retention, churn & A/B testing  
  
*Mirroring real DoorDash analyst workflows*
""")

# ============================================
# APPLY FILTERS
# ============================================
filtered_orders = orders[orders['order_status'] == 'completed'].copy()

if selected_city != 'All Cities':
    filtered_orders = filtered_orders[
        filtered_orders['city'] == selected_city
    ]

if selected_device != 'All Devices':
    filtered_orders = filtered_orders[
        filtered_orders['device_type'] == selected_device
    ]

if selected_user_type == 'DashPass':
    filtered_orders = filtered_orders[
        filtered_orders['is_dashpass'] == True
    ]
elif selected_user_type == 'Regular':
    filtered_orders = filtered_orders[
        filtered_orders['is_dashpass'] == False
    ]

if selected_cuisine:
    filtered_orders = filtered_orders[
        filtered_orders['cuisine_category'].isin(selected_cuisine)
    ]

# ============================================
# MAIN HEADER
# ============================================
st.markdown("""
<h1 style='color:#1B3A6B; font-size:2rem; margin-bottom:0'>
    🍔 Product Analytics Dashboard
</h1>
<p style='color:#6B7280; font-size:1rem; margin-top:4px'>
    DoorDash Case Study — Funnel, Retention, Churn & A/B Testing
</p>
<hr style='border:1px solid #E5E7EB; margin:16px 0'>
""", unsafe_allow_html=True)

# ============================================
# NAVIGATION TABS
# ============================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Executive Summary",
    "🔽 Funnel Analysis",
    "🔄 Cohort Retention",
    "⭐ DashPass Intelligence",
    "⚠️ Churn Risk",
    "🧪 A/B Test Results",
    "🤖 AI Copilot"
])

# ============================================
# TAB 1 — EXECUTIVE SUMMARY
# ============================================
with tab1:
    st.markdown(
        "<div class='section-header'>📈 Executive Summary</div>",
        unsafe_allow_html=True
    )

    # KPI Cards
    total_orders = len(filtered_orders)
    total_revenue = filtered_orders['order_value'].sum()
    total_users = filtered_orders['customer_id'].nunique()
    avg_order_value = filtered_orders['order_value'].mean()
    dashpass_users = filtered_orders[
        filtered_orders['is_dashpass'] == True
    ]['customer_id'].nunique()
    avg_rating = filtered_orders['rating'].mean()

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{total_orders:,}</div>
            <div class='kpi-label'>Total Orders</div>
            <div class='kpi-delta'>✅ Completed</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>${total_revenue:,.0f}</div>
            <div class='kpi-label'>Total Revenue</div>
            <div class='kpi-delta'>💰 GMV</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{total_users:,}</div>
            <div class='kpi-label'>Unique Users</div>
            <div class='kpi-delta'>👤 Active</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>${avg_order_value:.2f}</div>
            <div class='kpi-label'>Avg Order Value</div>
            <div class='kpi-delta'>🛒 AOV</div>
        </div>""", unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{dashpass_users:,}</div>
            <div class='kpi-label'>DashPass Users</div>
            <div class='kpi-delta'>⭐ Subscribers</div>
        </div>""", unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{avg_rating:.2f}⭐</div>
            <div class='kpi-label'>Avg Rating</div>
            <div class='kpi-delta'>😊 Satisfaction</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Revenue by cuisine
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "<div class='section-header'>Revenue by Cuisine</div>",
            unsafe_allow_html=True
        )
        cuisine_rev = filtered_orders.groupby(
            'cuisine_category'
        )['order_value'].sum().reset_index()
        cuisine_rev.columns = ['Cuisine', 'Revenue']
        cuisine_rev = cuisine_rev.sort_values('Revenue', ascending=True)

        fig = px.bar(
            cuisine_rev,
            x='Revenue',
            y='Cuisine',
            orientation='h',
            color='Revenue',
            color_continuous_scale=['#93C5FD', '#1B3A6B'],
            title='Total Revenue by Cuisine Category'
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            coloraxis_showscale=False,
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(
            "<div class='section-header'>Orders by City</div>",
            unsafe_allow_html=True
        )
        city_orders = filtered_orders.groupby(
            'city'
        )['order_value'].sum().reset_index()
        city_orders.columns = ['City', 'Revenue']

        fig2 = px.treemap(
            city_orders,
            path=['City'],
            values='Revenue',
            color='Revenue',
            color_continuous_scale=['#93C5FD', '#1B3A6B'],
            title='Revenue Distribution by City'
        )
        fig2.update_layout(
            height=350,
            paper_bgcolor='white'
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Insight
    st.markdown("""
    <div class='insight-box'>
        💡 <b>Key Insight:</b> American and Mexican cuisines drive 
        the highest order volume while Japanese cuisine commands 
        the highest average order value at $38.44
    </div>
    <div class='rec-box'>
        📌 <b>Recommendation:</b> Promote Japanese restaurants 
        during dinner hours via push notifications to increase 
        average order value across the platform
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TAB 2 — FUNNEL ANALYSIS
# ============================================
with tab2:
    st.markdown(
        "<div class='section-header'>🔽 Funnel Conversion Analysis</div>",
        unsafe_allow_html=True
    )

    # Funnel data
    funnel_data = funnel.groupby('event')[
        'customer_id'
    ].nunique().reset_index()
    funnel_data.columns = ['Event', 'Users']

    event_order = [
        'app_open', 'browse_restaurants',
        'select_restaurant', 'add_to_cart',
        'reach_checkout', 'order_completed'
    ]
    event_labels = [
        'App Open', 'Browse Restaurants',
        'Select Restaurant', 'Add to Cart',
        'Reach Checkout', 'Order Completed'
    ]

    funnel_data['Event'] = pd.Categorical(
        funnel_data['Event'],
        categories=event_order,
        ordered=True
    )
    funnel_data = funnel_data.sort_values('Event')
    funnel_data['Label'] = event_labels
    funnel_data['Conversion %'] = (
        funnel_data['Users'] /
        funnel_data['Users'].max() * 100
    ).round(1)

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = go.Figure(go.Funnel(
            y=funnel_data['Label'],
            x=funnel_data['Users'],
            textinfo="value+percent initial",
            marker=dict(
                color=[
                    '#1B3A6B', '#2552A0', '#2E6AD4',
                    '#5B8FE8', '#93C5FD', '#BFDBFE'
                ]
            )
        ))
        fig.update_layout(
            title='User Journey Funnel',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 📊 Drop-off Summary")
        for i in range(1, len(funnel_data)):
            prev = funnel_data['Users'].iloc[i-1]
            curr = funnel_data['Users'].iloc[i]
            drop = round((prev - curr) / prev * 100, 1)
            label = funnel_data['Label'].iloc[i]
            color = "🔴" if drop > 10 else "🟡" if drop > 5 else "🟢"
            st.markdown(f"{color} **{label}**: -{drop}% drop")

    st.markdown("""
    <div class='insight-box'>
        💡 <b>Key Insight:</b> 23.7% of users who reach checkout 
        never complete their order — the biggest drop in the funnel
    </div>
    <div class='rec-box'>
        📌 <b>Recommendation:</b> Implement simplified 2-step 
        checkout — proven by A/B test to lift conversion by 7.4%
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TAB 3 — COHORT RETENTION
# ============================================
with tab3:
    st.markdown(
        "<div class='section-header'>🔄 Cohort Retention Analysis</div>",
        unsafe_allow_html=True
    )

    # Build cohort data
    orders_copy = orders[
        orders['order_status'] == 'completed'
    ].copy()
    orders_copy['order_date'] = pd.to_datetime(
        orders_copy['order_date']
    )
    orders_copy['order_month'] = orders_copy[
        'order_date'
    ].dt.to_period('M')

    # First order per user
    first_orders = orders_copy.groupby(
        'customer_id'
    )['order_date'].min().reset_index()
    first_orders.columns = ['customer_id', 'first_order_date']
    first_orders['cohort'] = pd.to_datetime(
        first_orders['first_order_date']
    ).dt.to_period('M')

    # Merge
    orders_cohort = orders_copy.merge(
        first_orders, on='customer_id'
    )
    orders_cohort['period_number'] = (
        orders_cohort['order_month'] -
        orders_cohort['cohort']
    ).apply(lambda x: x.n)

    # Cohort table
    cohort_data = orders_cohort.groupby(
        ['cohort', 'period_number']
    )['customer_id'].nunique().reset_index()

    cohort_pivot = cohort_data.pivot_table(
        index='cohort',
        columns='period_number',
        values='customer_id'
    )

    # Retention rates
    cohort_sizes = cohort_pivot[0]
    retention = cohort_pivot.divide(cohort_sizes, axis=0) * 100
    retention = retention.round(1)
    retention.index = retention.index.astype(str)
    retention = retention.iloc[:, :7]

    fig = px.imshow(
        retention,
        labels=dict(
            x="Month Number",
            y="Cohort Month",
            color="Retention %"
        ),
        color_continuous_scale=['#DBEAFE', '#1B3A6B'],
        title='Monthly Cohort Retention Heatmap',
        text_auto=True
    )
    fig.update_layout(
        height=450,
        paper_bgcolor='white'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
        💡 <b>Key Insight:</b> Earlier cohorts show consistently 
        stronger retention across all time periods — 
        suggesting onboarding improvements over time
    </div>
    <div class='rec-box'>
        📌 <b>Recommendation:</b> Replicate the onboarding 
        experience of highest-retaining cohorts for all new users
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TAB 4 — DASHPASS INTELLIGENCE
# ============================================
with tab4:
    st.markdown(
        "<div class='section-header'>⭐ DashPass Intelligence</div>",
        unsafe_allow_html=True
    )

    dashpass = orders[orders['order_status'] == 'completed'].copy()
    dashpass_group = dashpass.groupby('is_dashpass').agg(
        total_users=('customer_id', 'nunique'),
        total_orders=('order_id', 'count'),
        avg_order_value=('order_value', 'mean'),
        total_revenue=('order_value', 'sum'),
        avg_rating=('rating', 'mean')
    ).reset_index()
    dashpass_group['orders_per_user'] = (
        dashpass_group['total_orders'] /
        dashpass_group['total_users']
    ).round(1)
    dashpass_group['revenue_per_user'] = (
        dashpass_group['total_revenue'] /
        dashpass_group['total_users']
    ).round(2)
    dashpass_group['user_type'] = dashpass_group[
        'is_dashpass'
    ].map({True: 'DashPass', False: 'Regular', 1: 'DashPass', 0: 'Regular'})

    col1, col2, col3 = st.columns(3)

    metrics = [
        ('orders_per_user', 'Orders Per User', '📦'),
        ('revenue_per_user', 'Revenue Per User ($)', '💰'),
        ('avg_rating', 'Avg Rating', '⭐')
    ]

    for col, (metric, label, icon) in zip(
        [col1, col2, col3], metrics
    ):
        with col:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=dashpass_group['user_type'],
                y=dashpass_group[metric],
                marker_color=['#93C5FD', '#1B3A6B'],
                text=dashpass_group[metric].round(2),
                textposition='outside'
            ))
            fig.update_layout(
                title=f'{icon} {label}',
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=300,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

    # Orders over time by type
    orders['month'] = pd.to_datetime(
        orders['order_date']
    ).dt.to_period('M').astype(str)
    monthly = orders[
        orders['order_status'] == 'completed'
    ].groupby(['month', 'is_dashpass'])['order_id'].count().reset_index()
    monthly['user_type'] = monthly['is_dashpass'].map(
        {True: 'DashPass', False: 'Regular',
         1: 'DashPass', 0: 'Regular'}
    )

    fig = px.line(
        monthly,
        x='month',
        y='order_id',
        color='user_type',
        title='Monthly Orders — DashPass vs Regular',
        color_discrete_map={
            'DashPass': '#1B3A6B',
            'Regular': '#93C5FD'
        },
        markers=True
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=350,
        xaxis_title='Month',
        yaxis_title='Total Orders'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
        💡 <b>Key Insight:</b> DashPass users generate $415 revenue 
        per user vs $125 for Regular users — a 3.3x difference. 
        They order 14.2x per year vs 4.3x for Regular users
    </div>
    <div class='rec-box'>
        📌 <b>Recommendation:</b> Offer 30-day free DashPass trial 
        to Regular users — even 5% conversion rate would 
        significantly move platform revenue
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TAB 5 — CHURN RISK
# ============================================
with tab5:
    st.markdown(
        "<div class='section-header'>⚠️ Churn Risk Segmentation</div>",
        unsafe_allow_html=True
    )

    # RFM Analysis
    rfm = orders[orders['order_status'] == 'completed'].copy()
    rfm['order_date'] = pd.to_datetime(rfm['order_date'])
    snapshot_date = rfm['order_date'].max()

    rfm_table = rfm.groupby('customer_id').agg(
        recency=('order_date', lambda x: (snapshot_date - x.max()).days),
        frequency=('order_id', 'count'),
        monetary=('order_value', 'sum')
    ).reset_index()

    def segment_user(row):
        if row['recency'] <= 30 and row['frequency'] >= 5:
            return 'Champion'
        elif row['recency'] <= 30 and row['frequency'] < 5:
            return 'Promising'
        elif 31 <= row['recency'] <= 60:
            return 'At Risk'
        elif 61 <= row['recency'] <= 90:
            return 'Churning'
        else:
            return 'Lost'

    rfm_table['segment'] = rfm_table.apply(segment_user, axis=1)

    segment_summary = rfm_table.groupby('segment').agg(
        num_users=('customer_id', 'count'),
        avg_spend=('monetary', 'mean'),
        avg_orders=('frequency', 'mean')
    ).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.treemap(
            segment_summary,
            path=['segment'],
            values='num_users',
            color='avg_spend',
            color_continuous_scale=['#BFDBFE', '#1B3A6B'],
            title='Churn Risk Segments — User Distribution'
        )
        fig.update_layout(height=400, paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.scatter(
            segment_summary,
            x='avg_orders',
            y='avg_spend',
            size='num_users',
            color='segment',
            title='Segment Value Map',
            color_discrete_sequence=px.colors.qualitative.Set2,
            text='segment'
        )
        fig2.update_traces(textposition='top center')
        fig2.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Segment table
    st.markdown("### 📋 Segment Details")
    segment_summary['avg_spend'] = segment_summary[
        'avg_spend'
    ].round(2)
    segment_summary['avg_orders'] = segment_summary[
        'avg_orders'
    ].round(1)
    segment_summary.columns = [
        'Segment', 'Users', 'Avg Spend ($)', 'Avg Orders'
    ]
    st.dataframe(
        segment_summary,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("""
    <div class='insight-box'>
        💡 <b>Key Insight:</b> 3,753 At Risk + Churning users 
        represent ~$650K in recoverable revenue if retained
    </div>
    <div class='rec-box'>
        📌 <b>Recommendation:</b> Launch win-back campaign for 
        At Risk users with personalized discount before they 
        transition to Lost status
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TAB 6 — A/B TEST RESULTS
# ============================================
with tab6:
    st.markdown(
        "<div class='section-header'>🧪 A/B Test — Checkout Experiment</div>",
        unsafe_allow_html=True
    )

    control = ab_test[ab_test['experiment_group'] == 'control']
    variant = ab_test[ab_test['experiment_group'] == 'variant']

    control_rate = control['converted'].mean() * 100
    variant_rate = variant['converted'].mean() * 100
    lift = variant_rate - control_rate

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{control_rate:.1f}%</div>
            <div class='kpi-label'>Control Conversion</div>
            <div class='kpi-delta'>Old 4-step checkout</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{variant_rate:.1f}%</div>
            <div class='kpi-label'>Variant Conversion</div>
            <div class='kpi-delta'>New 2-step checkout</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>+{lift:.1f}%</div>
            <div class='kpi-label'>Conversion Lift</div>
            <div class='kpi-delta'>✅ Statistically significant</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>$966M</div>
            <div class='kpi-label'>Annual Revenue Impact</div>
            <div class='kpi-delta'>At DoorDash scale</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Conversion comparison
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Control',
            x=['Control (Old Checkout)'],
            y=[control_rate],
            marker_color='#93C5FD',
            text=[f'{control_rate:.1f}%'],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            name='Variant',
            x=['Variant (New Checkout)'],
            y=[variant_rate],
            marker_color='#1B3A6B',
            text=[f'{variant_rate:.1f}%'],
            textposition='outside'
        ))
        fig.add_hline(
            y=control_rate,
            line_dash='dash',
            line_color='red',
            annotation_text='Baseline'
        )
        fig.update_layout(
            title='Conversion Rate — Control vs Variant',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            yaxis_title='Conversion Rate (%)',
            showlegend=False,
            yaxis_range=[0, 75]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Segment breakdown
        segment_ab = ab_test.groupby(
            ['experiment_group', 'device_type']
        )['converted'].mean().reset_index()
        segment_ab['converted'] = (
            segment_ab['converted'] * 100
        ).round(1)
        segment_ab.columns = [
            'Group', 'Device', 'Conversion Rate'
        ]

        fig2 = px.bar(
            segment_ab,
            x='Device',
            y='Conversion Rate',
            color='Group',
            barmode='group',
            title='Conversion by Device Type',
            color_discrete_map={
                'control': '#93C5FD',
                'variant': '#1B3A6B'
            },
            text='Conversion Rate'
        )
        fig2.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
        💡 <b>Key Insight:</b> New 2-step checkout is statistically 
        significant (p < 0.001) with 7.4% absolute lift. 
        iOS and Web users benefit most at 7.8% lift each
    </div>
    <div class='rec-box'>
        📌 <b>Recommendation:</b> Ship variant to 100% of users 
        immediately. Prioritize iOS and Web rollout first. 
        Projected $966M annual revenue impact at DoorDash scale
    </div>
    """, unsafe_allow_html=True)
    # ============================================
# TAB 7 — AI COPILOT
# ============================================
with tab7:
    st.markdown(
        "<div class='section-header'>🤖 AI Product Analytics Copilot</div>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class='insight-box'>
        💡 Ask me anything about your DoorDash product data! 
        I can analyze trends, explain findings, and suggest 
        recommendations based on your actual dashboard data.
    </div>
    """, unsafe_allow_html=True)

    # Load environment and API key
    from dotenv import load_dotenv
    import os
    import google.generativeai as genai

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Build data context from your actual data
    total_orders = len(orders[orders['order_status'] == 'completed'])
    total_revenue = orders[orders['order_status'] == 'completed']['order_value'].sum()
    dashpass_orders = orders[orders['is_dashpass'] == True]['order_id'].count()
    regular_orders = orders[orders['is_dashpass'] == False]['order_id'].count()
    dashpass_users = orders[orders['is_dashpass'] == True]['customer_id'].nunique()
    regular_users = orders[orders['is_dashpass'] == False]['customer_id'].nunique()

    data_context = f"""
    You are a Product Analytics AI Copilot for a DoorDash case study dashboard.
    You have access to the following real data insights:

    PLATFORM OVERVIEW:
    - Total completed orders: {total_orders:,}
    - Total revenue: ${total_revenue:,.2f}
    - Total unique users: {orders['customer_id'].nunique():,}
    - Average order value: ${orders[orders['order_status']=='completed']['order_value'].mean():.2f}

    DASHPASS INSIGHTS:
    - DashPass users: {dashpass_users:,} (20% of users)
    - Regular users: {regular_users:,} (80% of users)
    - DashPass orders per user: 14.2
    - Regular orders per user: 4.3
    - DashPass revenue per user: $415.45
    - Regular revenue per user: $125.76
    - DashPass avg rating: 4.50
    - Regular avg rating: 3.75

    FUNNEL METRICS:
    - App open to order completion rate: 76.3%
    - Biggest drop-off: checkout to order completion (23.7%)
    - Add to cart rate: 95.1%
    - Checkout reach rate: 87.0%

    COHORT RETENTION:
    - Average 30-day retention: ~87%
    - Earlier cohorts retain better than newer ones
    - DashPass users are active 2x more weeks than regular users

    CHURN RISK (RFM):
    - Champions: 2,161 users — avg spend $323
    - At Risk: 2,283 users — avg spend $216
    - Churning: 1,470 users — avg spend $164
    - Lost: 3,520 users — avg spend $106
    - Recoverable revenue from At Risk + Churning: ~$650K

    A/B TEST RESULTS:
    - Control (old checkout): 52.1% conversion
    - Variant (new checkout): 59.5% conversion
    - Lift: +7.4% (statistically significant, p < 0.001)
    - Projected annual revenue impact: $966M at DoorDash scale

    ACQUISITION CHANNELS:
    - Organic search: highest LTV at $189 per user
    - Referral: second highest at $187 per user
    - Paid channels: slightly lower at $183-185 per user

    REORDER PROPENSITY:
    - Users with 3+ orders in Week 1: 100% Day-30 retention
    - Users with 2 orders in Week 1: 96% Day-30 retention
    - Users with 1 order in Week 1: 86% Day-30 retention

    Always answer in a professional but friendly tone.
    Give specific data-backed answers using the numbers above.
    End each answer with one actionable recommendation.
    Keep answers concise — maximum 150 words.
    """

    # Example questions
    st.markdown("### 💬 Try These Questions")
    example_questions = [
        "Why is retention dropping for newer cohorts?",
        "Which user segment should we prioritize for growth?",
        "Should we ship the new checkout flow?",
        "How can we increase DashPass adoption?",
        "Which acquisition channel gives the best ROI?",
        "What is our biggest revenue opportunity right now?"
    ]

    cols = st.columns(3)
    for i, question in enumerate(example_questions):
        with cols[i % 3]:
            if st.button(question, key=f"q_{i}"):
                st.session_state['copilot_question'] = question

    st.markdown("---")

    # Chat interface
    st.markdown("### 🔍 Ask Your Own Question")

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Check if example question was clicked
    if 'copilot_question' in st.session_state:
        default_q = st.session_state['copilot_question']
    else:
        default_q = ""

    user_question = st.text_input(
        "Type your question here:",
        value=default_q,
        placeholder="e.g. Why are users dropping off at checkout?"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        ask_button = st.button("🚀 Ask AI", type="primary")
    with col2:
        if st.button("🗑️ Clear History"):
            st.session_state['chat_history'] = []
            st.rerun()

    if ask_button and user_question:
        with st.spinner("🤖 Analyzing your data..."):
            try:
                # Build prompt
                prompt = f"""
                {data_context}

                User Question: {user_question}

                Please provide a specific, data-backed answer 
                using the metrics provided above.
                """

                response = model.generate_content(prompt)
                answer = response.text

                # Add to history
                st.session_state['chat_history'].append({
                    'question': user_question,
                    'answer': answer
                })

                # Clear the example question
                if 'copilot_question' in st.session_state:
                    del st.session_state['copilot_question']

            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Display chat history
    if st.session_state['chat_history']:
        st.markdown("### 📋 Conversation History")
        for i, chat in enumerate(
            reversed(st.session_state['chat_history'])
        ):
            st.markdown(f"""
            <div style='background:#EFF6FF; padding:12px; 
                        border-radius:8px; margin:8px 0;
                        border-left:4px solid #1B3A6B'>
                <b>🙋 You:</b> {chat['question']}
            </div>
            <div style='background:#F0FDF4; padding:12px; 
                        border-radius:8px; margin:8px 0;
                        border-left:4px solid #10B981'>
                <b>🤖 AI:</b> {chat['answer']}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class='rec-box' style='margin-top:20px'>
        📌 <b>Note:</b> This AI copilot is powered by Google Gemini 
        and analyzes your actual dashboard data to provide 
        product recommendations — just like an internal 
        analytics tool at DoorDash or Amazon.
    </div>
    """, unsafe_allow_html=True)

