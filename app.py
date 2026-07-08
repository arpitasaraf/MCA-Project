import streamlit as st
import time
import random

# Page config configuration
st.set_page_config(
    page_title="KPI Insight - Live Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom premium styling matching the Angular KPI Insight dark mode theme
st.markdown("""
<style>
/* Import Outfit and Inter fonts */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Main application background color and font families */
.stApp {
    background-color: #0b0f19 !important;
    font-family: 'Outfit', 'Inter', sans-serif !important;
}

/* Custom premium card design for the login container */
.premium-card {
    background-color: #121826;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.05);
    margin: 40px auto;
    max-width: 480px;
}

/* Header style within the card */
.premium-card h2 {
    color: #f8fafc;
    font-weight: 800;
    font-size: 24px;
    text-align: center;
    margin-bottom: 5px;
    letter-spacing: -0.5px;
}

.premium-subtitle {
    color: #94a3b8;
    font-size: 13px;
    text-align: center;
    margin-bottom: 25px;
}

/* Custom CSS styling overrides for Streamlit native text inputs */
div[data-baseweb="input"] {
    background-color: #0b0f19 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}

div[data-baseweb="input"] input {
    color: #f8fafc !important;
    font-size: 14px !important;
}

label[data-testid="stWidgetLabel"] p {
    color: #94a3b8 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* Custom styling for Streamlit button elements */
div.stButton button {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    width: 100% !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35) !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

div.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(99, 102, 241, 0.5) !important;
    background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
}

div.stButton button:active {
    transform: translateY(0) !important;
}

/* Back navigation button styling override */
div.stButton button[key*="back"] {
    background: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #94a3b8 !important;
    box-shadow: none !important;
}

div.stButton button[key*="back"]:hover {
    background: rgba(99, 102, 241, 0.08) !important;
    color: #6366f1 !important;
    border-color: rgba(99, 102, 241, 0.3) !important;
}

/* Custom KPI card design for the dashboard layout */
.kpi-card {
    background-color: #121826;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease;
}

.kpi-card:hover {
    border-color: rgba(99, 102, 241, 0.25);
    transform: translateY(-2px);
}

.kpi-title {
    font-size: 11px;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 12px;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}

.kpi-change-up {
    font-size: 12px;
    color: #10b981;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.kpi-change-down {
    font-size: 12px;
    color: #f43f5e;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
</style>
""", unsafe_allow_html=True)

# Initialize Streamlit session state properties
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_step" not in st.session_state:
    st.session_state.login_step = 1

if "company_name" not in st.session_state:
    st.session_state.company_name = ""
if "company_id" not in st.session_state:
    st.session_state.company_id = ""
if "username" not in st.session_state:
    st.session_state.username = ""
if "email" not in st.session_state:
    st.session_state.email = ""

def fetch_live_kpi_stream():
    """Generates continuous live stream updates for metric properties."""
    base_revenue = 48592
    base_users = 2847
    base_conversion = 3.24
    base_session_sec = 272  # Equivalent to 4m 32s
    
    while True:
        rev_delta = random.randint(-150, 250)
        users_delta = random.randint(-10, 15)
        conv_delta = round(random.uniform(-0.05, 0.08), 2)
        sess_delta = random.randint(-5, 5)
        
        yield {
            "revenue": base_revenue + rev_delta,
            "revenue_change": f"{'+' if rev_delta >= 0 else ''}{round(rev_delta / base_revenue * 100, 2)}%",
            "revenue_up": rev_delta >= 0,
            
            "active_users": base_users + users_delta,
            "users_change": f"{'+' if users_delta >= 0 else ''}{round(users_delta / base_users * 100, 2)}%",
            "users_up": users_delta >= 0,
            
            "conversion_rate": round(base_conversion + conv_delta, 2),
            "conversion_change": f"{'+' if conv_delta >= 0 else ''}{conv_delta}%",
            "conversion_up": conv_delta >= 0,
            
            "session_duration": base_session_sec + sess_delta,
            "session_change": f"{'+' if sess_delta >= 0 else ''}{sess_delta}s",
            "session_up": sess_delta >= 0,
        }
        time.sleep(1.0)

# Application Routing / Guard Checks
if not st.session_state.logged_in:
    # Render Step 1 or Step 2 multi-step form process
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<h2>KPI Insight</h2>', unsafe_allow_html=True)
    st.markdown('<p class="premium-subtitle">Sign in to access your dashboard</p>', unsafe_allow_html=True)
    
    current_step = st.session_state.login_step
    
    # Custom HTML Step indicator representation
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 25px;">
        <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #6366f1; letter-spacing: 1px;">
            Step {current_step} of 2
        </span>
        <div style="display: flex; align-items: center; gap: 6px; margin-top: 8px;">
            <div style="width: 8px; height: 8px; border-radius: 50%; background: #6366f1; box-shadow: 0 0 8px #6366f1;"></div>
            <div style="width: 30px; height: 2px; background: {'#6366f1' if current_step == 2 else 'rgba(255, 255, 255, 0.15)'};"></div>
            <div style="width: 8px; height: 8px; border-radius: 50%; background: {'#6366f1' if current_step == 2 else 'rgba(255, 255, 255, 0.15)'}; {'box-shadow: 0 0 8px #6366f1;' if current_step == 2 else ''}"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if current_step == 1:
        company_name = st.text_input("Company Name", value=st.session_state.company_name, placeholder="Enter Company Name")
        company_id = st.text_input("Company ID / CIN", value=st.session_state.company_id, placeholder="Enter Company ID / CIN")
        
        st.session_state.company_name = company_name
        st.session_state.company_id = company_id
        
        # Enable next step only if values are present
        next_disabled = not (company_name.strip() and company_id.strip())
        if st.button("Next Step", disabled=next_disabled):
            st.session_state.login_step = 2
            st.rerun()

    elif current_step == 2:
        username = st.text_input("Username", value=st.session_state.username, placeholder="Enter Username")
        email = st.text_input("Email Address", value=st.session_state.email, placeholder="name@company.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        st.session_state.username = username
        st.session_state.email = email
        
        # Credentials validation
        login_disabled = not (username.strip() and email.strip() and len(password) >= 8)
        
        if st.button("Sign In", disabled=login_disabled):
            if st.session_state.company_name and st.session_state.company_id:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Authentication session mismatch. Please restart login.")
        
        if st.button("Back to Company Details", key="back_btn"):
            st.session_state.login_step = 1
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Render Step 2: Real-time Live Dashboard
    # Sidebar user profile identity card
    with st.sidebar:
        user_initials = (st.session_state.username.strip()[:2].upper() 
                         if st.session_state.username else "AD")
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 20px;">
            <div style="width: 60px; height: 60px; border-radius: 16px; background: linear-gradient(135deg, #6366f1 0%, #a78bfa 100%); display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; color: white; font-weight: 800; font-size: 20px; box-shadow: 0 8px 24px rgba(99, 102, 241, 0.25);">
                {user_initials}
            </div>
            <h4 style="color: #f8fafc; margin: 0 0 2px 0; font-size: 16px; font-weight: 700;">{st.session_state.username}</h4>
            <p style="color: #94a3b8; font-size: 12px; margin: 0;">{st.session_state.company_name}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.login_step = 1
            st.rerun()

    # Dashboard Main Headers
    st.markdown(f"""
    <div style="margin-bottom: 30px;">
        <h1 style="color: #f8fafc; font-weight: 800; margin-bottom: 4px; font-family: 'Outfit'; font-size: 32px; letter-spacing: -0.5px;">Dashboard</h1>
        <p style="color: #94a3b8; font-size: 14px; margin: 0;">
            Monitoring live parameters for <strong>{st.session_state.company_name}</strong> (ID: {st.session_state.company_id})
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Empty container to dynamically mount and loop the live stream content
    dashboard_block = st.empty()

    # Loop live kpi stream inside the container
    for kpis in fetch_live_kpi_stream():
        with dashboard_block.container():
            # Generate 4 Column Layout for KPI cards
            c1, c2, c3, c4 = st.columns(4)
            
            # Format Session Duration helper
            mins = kpis["session_duration"] // 60
            secs = kpis["session_duration"] % 60
            session_str = f"{mins}m {secs}s"
            
            # Card 1: Revenue
            with c1:
                change_class = "kpi-change-up" if kpis["revenue_up"] else "kpi-change-down"
                arrow = "▲" if kpis["revenue_up"] else "▼"
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Total Revenue</div>
                    <div class="kpi-value">${kpis["revenue"]:,}</div>
                    <div class="{change_class}">{arrow} {kpis["revenue_change"]}</div>
                </div>
                """, unsafe_allow_html=True)

            # Card 2: Active Users
            with c2:
                change_class = "kpi-change-up" if kpis["users_up"] else "kpi-change-down"
                arrow = "▲" if kpis["users_up"] else "▼"
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Active Users</div>
                    <div class="kpi-value">{kpis["active_users"]:,}</div>
                    <div class="{change_class}">{arrow} {kpis["users_change"]}</div>
                </div>
                """, unsafe_allow_html=True)

            # Card 3: Conversion Rate
            with c3:
                change_class = "kpi-change-up" if kpis["conversion_up"] else "kpi-change-down"
                arrow = "▲" if kpis["conversion_up"] else "▼"
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Conversion Rate</div>
                    <div class="kpi-value">{kpis["conversion_rate"]}%</div>
                    <div class="{change_class}">{arrow} {kpis["conversion_change"]}</div>
                </div>
                """, unsafe_allow_html=True)

            # Card 4: Avg Session
            with c4:
                change_class = "kpi-change-up" if kpis["session_up"] else "kpi-change-down"
                arrow = "▲" if kpis["session_up"] else "▼"
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Avg. Session Duration</div>
                    <div class="kpi-value">{session_str}</div>
                    <div class="{change_class}">{arrow} {kpis["session_change"]}</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Sub-layout charts & lists
            cc1, cc2 = st.columns([2, 1])
            with cc1:
                st.markdown("""
                <div style="background-color: #121826; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 20px; margin-bottom: 12px;">
                    <h5 style="color: #f8fafc; font-weight: 600; margin: 0 0 15px 0; font-size: 14px;">Revenue History Trend (Streaming)</h5>
                </div>
                """, unsafe_allow_html=True)
                # Render simple Streamlit line chart representing live streaming history
                hist_data = [18200, 22400, 19800, 24100, 28500, 32200, 29800, 35100, 38400, 42100, 45200, kpis["revenue"]]
                st.line_chart(hist_data)
                
            with cc2:
                st.markdown(f"""
                <div style="background-color: #121826; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 20px; height: 100%;">
                    <h5 style="color: #f8fafc; font-weight: 600; margin: 0 0 15px 0; font-size: 14px;">Recent System Events</h5>
                    <div style="display: flex; flex-direction: column; gap: 14px; font-size: 13px; color: #cbd5e1;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="color: #10b981; font-size: 14px;">●</span> Q2 Revenue Target of $48K Achieved!
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="color: #f59e0b; font-size: 14px;">●</span> Server load spikes observed
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="color: #6366f1; font-size: 14px;">●</span> User registrations (+142 today)
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="color: #ef4444; font-size: 14px;">●</span> 3 bug fixes deployed to production
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
