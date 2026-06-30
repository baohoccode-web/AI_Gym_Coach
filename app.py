from re import S
import streamlit as st

#1: page config
st.set_page_config(
    page_title="AI Gym Progress Coach",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
    )

#2: sidebar navigation
st.sidebar.title("🏋️ AI Gym Coach")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Log Workout", "Progress", "AI Coach", "Profile"],
)

#3: temporary page function
def show_dashboard():
    st.title("Dashboard")
    st.write("Welcome to your AI Gym Coach dashboard!")
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Weekly Volume", "100 kg")

    with col2:
        st.metric("Session This Week", "4")

    with col3:
        st.metric("Latest PR", "100 kg")

    with col4:
        st.metric("Plateau Risk", "Low")

    st.divider()
    
    left_column, right_column = st.columns([2, 1])
    with left_column:
        st.subheader("Progress Chart")
        st.info("Visualize your progress over time")

    with right_column:
        st.subheader("AI Summary")
        st.info("AI-generated insights and recommendations")
def show_log_workout():
    st.title("Log Workout")
    st.write("Track your workouts")
    
    with st.form("log_workout_form"):
        date = st.date_input("Workout Date")
        workout_type = st.selectbox("Workout Type", ["Push", "Pull", "Leg", "Upper", "Lower", "Full Body", "Custom"],
        )
        exercise = st.text_input("Exercise Name", placeholder="Ví dụ: Bench Press")
        set_number = st.number_input("Set Number", min_value=1, step=1)
        weight = st.number_input("Weight (kg)", min_value=0.0, step=2.5)
        reps = st.number_input("Reps", min_value=1, step=1)
        rpe = st.slider("RPE", min_value=1.0, max_value=10.0, step=0.5)
        notes = st.text_area("Notes", placeholder="Ghi chú nếu có...")

        submitted = st.form_submit_button("Save Workout")
    if submitted:
        st.success("Workout logged successfully!")
        st.write(
            {
                "date": str(date),
                "workout_type": workout_type,
                "exercise": exercise,
                "set_number": set_number,
                "weight": weight,
                "reps": reps,
                "rpe": rpe,
                "notes": notes,  
            }
        )
def show_progress():
        st.title("Progress")
        st.write("Track your progress over time")

        selected_exercise = st.selectbox("Select Exercise",
        ["Bench Press", "Squat", "Deadlift", "Overhead Press", "Barbell Row", "Custom"],
        )
        
        time_range = st.selectbox("Time Range", ["Week", "Month", "Quarter", "Year", "All Time"],
        )

        st.info(f"Showing progress for {selected_exercise} over {time_range}")

        st.subheader("Progress Chart")
        st.info("Later, we will add Estimated 1RM, Volume, and Average RPE")

def show_ai_coach():
        st.title("AI Coach")
        st.write("Get personalized training advice and progress tracking")

        selected_exercise = st.selectbox("Select Exercise to Analyze",
        ["Bench Press", "Squat", "Deadlift", "Overhead Press", "Barbell Row", "Custom"],
        )

        analyze_button = st.button("Analyze")

        if analyze_button:
            st.subheader(f"AI Analysis for {selected_exercise}")

            st.metric("Plateau Risk", "Low")
            st.subheader("Reasoning")
            st.info("Later AI will complain why this excercise is plateauing or not")

            st.subheader("Recommendation")
            st.success("Later AI will recommend what to do to improve the exercise")
        
def show_profile():
    st.title("Profile")
    st.write("Personal profile information")

    name = st.text_input("Name", placeholder="Your Name")
    goal = st.selectbox("Goal", ["Strength", "Hypertrophy", "Endurance","Fat Loss", "Custom"],
    )
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced", "Custom"],
    )
    bodyweight = st.number_input("Bodyweight (kg)", min_value=0.0, step=0.5)
    frequency = st.selectbox("Training Frequency per Week", ["3x/week", "4x/week", "5x/week", "Custom"],
    )

    if st.button("Save Profile"):
        st.success("Profile saved successfully!")
        st.write(
            {
                "name": name,
                "goal": goal,
                "level": level,
                "bodyweight": bodyweight,
                "frequency": frequency,
            }
        )

#4. router
if page == "Dashboard":
    show_dashboard()
elif page == "Log Workout":
    show_log_workout()
elif page == "Progress":
    show_progress()
elif page == "AI Coach":
    show_ai_coach()
elif page == "Profile":
    show_profile()
