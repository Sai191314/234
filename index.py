import streamlit as st
import random
import base64

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

sakura = ""

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Saikoto - Hiragana Memory Lab",
    page_icon="1002.jpeg",
    layout="centered"
)

# ==================================
# CSS
# ==================================

st.markdown("""
<style>
h1 a {
display:none !important;
}


.stApp {
background: linear-gradient(
135deg,
#fff7f7,
#ffeaea,
#fff0f5
);
}



.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    color: #d63384;
    margin-top: -10;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 30px;
}

.quiz-card {
    background: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.hiragana-char {
    font-size: 90px;
    font-weight: bold;
    color: #e63946;
}

.score-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}

.footer {
    text-align:center;
    color:#888;
    margin-top:30px;
    font-size:14px;
}

/* --- Logo lockup: sits tight above the title, centered --- */
/* Targets the real element st.image() renders (data-testid="stImage"). */
[data-testid="stImage"] {
display: flex;
justify-content: center;
}
.main-title{
margin-top: -10px;
font-size:2.8rem;
}

div[role="radiogroup"] {
    background: white;
    padding: 8px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

div[role="radiogroup"] label {
    border-radius: 12px !important;
    padding: 8px 18px !important;
    transition: all 0.25s ease;
}

div[role="radiogroup"] label:hover {
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# ==================================
# DATA
# ==================================

hiragana = {
    "あ": "a",
    "い": "i",
    "う": "u",
    "え": "e",
    "お": "o",
    "か": "ka",
    "き": "ki",
    "く": "ku",
    "け": "ke",
    "こ": "ko",
    "さ": "sa",
    "し": "shi",
    "す": "su",
    "せ": "se",
    "そ": "so",
    "た": "ta",
    "ち": "chi",
    "つ": "tsu",
    "て": "te",
    "と": "to",
    "な": "na",
    "に": "ni",
    "ぬ": "nu",
    "ね": "ne",
    "の": "no",
    "は": "ha",
    "ひ": "hi",
    "ふ": "fu",
    "へ": "he",
    "ほ": "ho",
    "ま": "ma",
    "み": "mi",
    "む": "mu",
    "め": "me",
    "も": "mo",
    "や": "ya",
    "ゆ": "yu",
    "よ": "yo",
    "ら": "ra",
    "り": "ri",
    "る": "ru",
    "れ": "re",
    "ろ": "ro",
    "わ": "wa",
    "を": "wo"
}

# ==================================
# SESSION STATE
# ==================================

if "score" not in st.session_state:
    st.session_state.score = 0

if "mistakes" not in st.session_state:
    st.session_state.mistakes = {}

if "mastery" not in st.session_state:
    st.session_state.mastery = {
        char: 50 for char in hiragana.keys()
    }

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "level" not in st.session_state:
    st.session_state.level = 1
if "streak" not in st.session_state:
    st.session_state.streak = 0

if "best_streak" not in st.session_state:
    st.session_state.best_streak = 0
if "badges" not in st.session_state:
    st.session_state.badges = []

if "current" not in st.session_state:
    st.session_state.current = random.choice(list(hiragana.keys()))
if "hunt_target" not in st.session_state:
    st.session_state.hunt_target = random.choice(
        list(hiragana.keys())
    )
if "hunt_options" not in st.session_state:
    target = st.session_state.hunt_target
    st.session_state.hunt_options = (
        random.sample(
            [c for c in hiragana.keys() if c != target],
            3
        ) + [target]
    )
    random.shuffle(
        st.session_state.hunt_options
    )



if "feedback" not in st.session_state:
    st.session_state.feedback = ""
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)
# ==================================
# HEADER
# ==================================

col1, col2 = st.columns([1,4])
with col1:
    st.markdown("<div style='margin-top:-15px'",
unsafe_allow_html = True)
    st.image("1002.jpeg",width=100)
    st.markdown("</div>", unsafe_allow_html = True)
with col2:
    st.markdown("""
<div style='padding-top:4px;'>
<h1 style='margin-bottom:0;'>Saikoto</h1>
<p style='margin-top:0; color:#666;'>
Learn Japanese Smarter, Not Harder
</p>
</div>
""", unsafe_allow_html = True)



mode = st.radio(
    "",
    ["🧠 Quiz", "🎯 Hunt"],
    horizontal=True
)



total_mastery = sum(
    st.session_state.mastery.values()
)

max_mastery = len(hiragana) * 100

progress = total_mastery / max_mastery

st.progress(progress)

st.caption(
    f"🌸 Japanese Journey: {progress*100:.1f}%"
)

st.session_state.level = (
    st.session_state.xp // 100
) + 1

st.markdown(
f""" 
<div style="
background: white;
padding: 12px;
border-radius:15px;
text-align:center;
font-size: 20px;
margin-bottom: 20px;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
">
🔥 {st.session_state.streak}
&nbsp;&nbsp;&nbsp;
👑 {st.session_state.best_streak}
&nbsp;&nbsp;&nbsp;
⭐ {st.session_state.xp}
&nbsp;&nbsp;&nbsp;
🏆 {st.session_state.level}

</div>
""",
unsafe_allow_html = True
)


if mode == "🎯 Hunt":

    target = st.session_state.hunt_target
    target_romaji = hiragana[target]

    st.markdown("🎯 Character Hunt")
    if st.session_state.feedback:
        if"✅" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)

    st.info(f"Find: {target_romaji}")

    options = st.session_state.hunt_options

    cols = st.columns(2)

    for i, char in enumerate(options):

        with cols[i % 2]:

            if st.button(
                char,
                key=f"hunt_{i}",
                use_container_width=True
            ):
                
                if char == target:
                    st.session_state.feedback = "✅ Nice catch!"
                    st.session_state.score += 1
                    st.session_state.xp += 3
                    st.session_state.streak += 1
                    st.session_state.mastery[target] = min(
                        100,
                        st.session_state.mastery[target] +5
                    )
                    if st.session_state.streak > st.session_state.best_streak:
                        st.session_state.best_streak = (
                            st.session_state.streak
                        )
                else:
                    st.session_state.feedback = (f"❌ Wrong! {target} = {target_romaji}")
                    st.session_state.streak = 0
                    st.session_state.mastery[target] = max(
                        0,
                        st.session_state.mastery[target] -10

                    )
                    st.session_state.mistakes[target] = (
                        st.session_state.mistakes.get(target, 0) + 1
                    )

                st.session_state.hunt_target = random.choice(
                    list(hiragana.keys())
                )
                new_target = st.session_state.hunt_target
                st.session_state.hunt_options = (
                    random.sample(
                        [c for c in hiragana.keys() 
                         if c != new_target],
                        3
                    ) + [new_target]
                )
                random.shuffle(
                    st.session_state.hunt_options
                )


                st.rerun()



if mode == "🧠 Quiz":

    st.markdown(
        f"""
        <div class="quiz-card">
            <div class="hiragana-char">
                {st.session_state.current}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.session_state.feedback:
        if"✅" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)

    with st.form("quiz_form", clear_on_submit=True):

        answer = st.text_input(
            "Enter Romaji",
            key="answer_box",
            placeholder="Example: a, ka, shi..."
        )

        submitted = st.form_submit_button(
            "✨ Check Answer",
            use_container_width=True
        )

    if submitted:
        current = st.session_state.current
        correct = hiragana[current]

        if answer.lower().strip() == correct:
            st.session_state.feedback = "✅ Correct!"

            st.session_state.score += 1
            st.session_state.xp += 5

            st.session_state.streak += 1

            if st.session_state.streak > st.session_state.best_streak:
             
             st.session_state.best_streak = (
                 st.session_state.streak
             )

            st.session_state.mastery[current] = min(
                100,
                st.session_state.mastery[current] + 10
            )
        else:
            st.session_state.feedback = f"❌ {current} = {correct}"

            st.session_state.streak = 0

            st.session_state.mastery[current] = max(
                0,
                st.session_state.mastery[current] - 15
            )
            st.session_state.mistakes[current] = (
                st.session_state.mistakes.get(current, 0) + 1
            )
        next_char = random.choice(
            list(hiragana.keys())
        )
        while next_char == current:
            next_char = random.choice(
                list(hiragana.keys())
            )
        st.session_state.current = next_char
        st.rerun()

# ==================================
# BADGES
# ==================================

if (
    st.session_state.score >= 1
    and "🌱 First Step" not in st.session_state.badges
):
    st.session_state.badges.append("🌱 First Step")

if (
    st.session_state.score >= 10
    and "🎌 Hiragana Rookie" not in st.session_state.badges
):
    st.session_state.badges.append("🎌 Hiragana Rookie")

if (
    st.session_state.best_streak >= 5
    and "🔥 Combo Master" not in st.session_state.badges
):
    st.session_state.badges.append("🔥 Combo Master")

if (
    st.session_state.level >= 5
    and "⚔️ Study Warrior" not in st.session_state.badges
):
    st.session_state.badges.append("⚔️ Study Warrior")

st.markdown("### 🏅 Achievements")

if st.session_state.badges:

    cols = st.columns(2)

    for i, badge in enumerate(
        st.session_state.badges
    ):
        cols[i % 2].success(badge)

else:
    st.info(
        "No badges unlocked yet."
    )

# ==================================
# SCORE
# ==================================

st.markdown("### 📊 Progress")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Correct Answers",
        value=st.session_state.score
    )

with col2:
    st.metric(
        label="Characters Tracked",
        value=len(st.session_state.mistakes)
    )



st.markdown("### 🎯 Today's Focus")

weakest = sorted(
    st.session_state.mastery.items(),
    key=lambda x: x[1]
)[:5]

for char, score in weakest:

    st.write(f"**{char}**")
    st.progress(score / 100)


# ==================================
# CONFUSION DETECTOR
# ==================================

st.markdown("### ⚠️ Hiragana Trouble Zone")

if st.session_state.mistakes:

    sorted_chars = sorted(
        st.session_state.mistakes.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for char, count in sorted_chars:
        st.progress(min(count / 10, 1.0))
        st.write(
            f"**{char}** → {count} mistake(s)"
        )

else:
    st.info(
        "No mistakes yet. Keep going!"
    )

# ==================================
# FOOTER
# ==================================

st.markdown(
    """
    <div class="footer">
        Made with ❤️ by Saikoto • Japanese Learning Lab
    </div>
    """,
    unsafe_allow_html=True
)