import streamlit as st
import random
import time
import math
import io
import wave
import struct
import base64


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Aditya's Games World",
    page_icon="🎮",
    layout="centered"
)


# ============================================================
# GAME SETTINGS
# ============================================================

TOTAL_ROUNDS = 10

WEAPONS = {
    "rock": "🪨",
    "paper": "📄",
    "scissor": "✂️"
}


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "started": False,
    "round": 1,
    "user_wins": 0,
    "computer_wins": 0,
    "ties": 0,
    "user_choice": None,
    "computer_choice": None,
    "battle_started": False,
    "game_over": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# VIOLIN MUSIC
# ============================================================

def make_violin_music():

    sample_rate = 44100
    duration = 8.0

    audio = io.BytesIO()

    with wave.open(audio, "wb") as wav:

        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        frames = []

        notes = [
            293.66,
            329.63,
            392.00,
            440.00,
            392.00,
            329.63,
            293.66,
            261.63
        ]

        note_length = duration / len(notes)

        for i in range(int(sample_rate * duration)):

            t = i / sample_rate

            note_index = min(
                int(t / note_length),
                len(notes) - 1
            )

            frequency = notes[note_index]

            local_time = t % note_length

            # Violin vibrato
            vibrato = (
                1
                + 0.004 * math.sin(
                    2 * math.pi * 5 * t
                )
            )

            freq = frequency * vibrato

            # Violin-like harmonics
            violin = (
                0.55 * math.sin(
                    2 * math.pi * freq * t
                )
                + 0.25 * math.sin(
                    2 * math.pi * freq * 2 * t
                )
                + 0.12 * math.sin(
                    2 * math.pi * freq * 3 * t
                )
                + 0.06 * math.sin(
                    2 * math.pi * freq * 4 * t
                )
            )

            # Attack
            attack = min(
                local_time / 0.12,
                1
            )

            # Release
            release = min(
                (note_length - local_time) / 0.20,
                1
            )

            envelope = max(
                0,
                min(attack, release)
            )

            value = (
                violin
                * envelope
                * 0.20
            )

            value = max(
                -1,
                min(1, value)
            )

            frames.append(
                struct.pack(
                    "<h",
                    int(value * 30000)
                )
            )

        wav.writeframes(
            b"".join(frames)
        )

    audio.seek(0)

    return audio.getvalue()


# ============================================================
# SNIPER SOUND EFFECT
# ============================================================

def make_sniper_sound():

    sample_rate = 44100
    duration = 0.9

    audio = io.BytesIO()

    with wave.open(audio, "wb") as wav:

        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        frames = []

        for i in range(
            int(sample_rate * duration)
        ):

            t = i / sample_rate

            # Sharp crack
            crack = (
                math.exp(-110 * t)
                * (
                    math.sin(
                        2 * math.pi * 2100 * t
                    )
                    + 0.75 * math.sin(
                        2 * math.pi * 3200 * t
                    )
                    + 0.45 * math.sin(
                        2 * math.pi * 4700 * t
                    )
                )
            )

            # Deep blast
            boom = (
                math.exp(-7 * t)
                * (
                    math.sin(
                        2 * math.pi * 55 * t
                    )
                    + 0.55 * math.sin(
                        2 * math.pi * 90 * t
                    )
                    + 0.25 * math.sin(
                        2 * math.pi * 140 * t
                    )
                )
            )

            # Bullet whoosh
            whoosh = (
                math.exp(-14 * t)
                * math.sin(
                    2 * math.pi * 700 * t
                )
            )

            # Echo
            if t > 0.20:

                echo_time = t - 0.20

                echo = (
                    math.exp(-9 * echo_time)
                    * math.sin(
                        2
                        * math.pi
                        * 240
                        * echo_time
                    )
                )

            else:
                echo = 0

            # Combine sounds
            value = (
                0.72 * crack
                + 0.68 * boom
                + 0.18 * whoosh
                + 0.22 * echo
            )

            value = max(
                -1,
                min(1, value)
            )

            frames.append(
                struct.pack(
                    "<h",
                    int(value * 30000)
                )
            )

        wav.writeframes(
            b"".join(frames)
        )

    audio.seek(0)

    return audio.getvalue()


VIOLIN = make_violin_music()

SNIPER = make_sniper_sound()

VIOLIN_BASE64 = base64.b64encode(
    VIOLIN
).decode("utf-8")


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 15% 15%,
            #352c80 0%,
            transparent 32%
        ),
        radial-gradient(
            circle at 85% 20%,
            #702c7d 0%,
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 90%,
            #006d77 0%,
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #080b20,
            #111936,
            #090b1c
        );

    color: white;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 900;
    color: white;

    text-shadow:
        0 0 12px #00eaff,
        0 0 30px #7b2cff;

    margin: 12px 0 5px 0;
}

.subtitle {
    text-align: center;
    color: #dce7ff;
    font-size: 18px;
    margin-bottom: 25px;
}

.score-box {
    background: rgba(255,255,255,0.10);

    border:
        1px solid
        rgba(255,255,255,0.25);

    border-radius: 18px;

    padding: 12px;

    text-align: center;
}

.score-number {
    font-size: 30px;
    font-weight: 900;
}

.round-text {
    text-align: center;

    color: white;

    font-size: 22px;

    font-weight: 900;

    margin: 18px 0;
}

div.stButton > button {

    width: 100%;

    min-height: 65px;

    border-radius: 18px;

    background:
        rgba(255,255,255,0.12);

    color: white;

    border:
        1px solid
        rgba(255,255,255,0.30);

    font-size: 19px;

    font-weight: 900;
}

div.stButton > button:hover {

    background:
        rgba(255,255,255,0.23);

    transform:
        translateY(-3px);

}

.battle-box {

    text-align: center;

    background:
        rgba(255,255,255,0.08);

    border:
        2px solid
        rgba(255,255,255,0.22);

    border-radius: 24px;

    padding: 22px;

    margin:
        10px 0 20px 0;
}

.fighter-name {

    color: white;

    font-size: 20px;

    font-weight: 900;
}

.hand {

    display: inline-block;

    font-size: 75px;

    margin: 12px;
}

.shake {

    animation:
        shake 0.32s infinite alternate;
}

@keyframes shake {

    from {
        transform:
            rotate(-17deg)
            translateX(-8px);
    }

    to {
        transform:
            rotate(17deg)
            translateX(8px);
    }

}

.ready {

    text-align: center;

    color: white;

    font-size: 43px;

    font-weight: 900;

    text-shadow:
        0 0 12px #00eaff,
        0 0 25px #7b2cff;
}

.shoot {

    text-align: center;

    color: white;

    font-size: 38px;

    font-weight: 900;

    text-shadow:
        0 0 12px #ffae00,
        0 0 25px #ff4500;
}

.explosion {

    text-align: center;

    font-size: 90px;

    animation:
        explode 0.55s ease-out;
}

@keyframes explode {

    0% {
        transform:
            scale(0.2)
            rotate(-30deg);

        opacity: 0;
    }

    50% {
        transform:
            scale(1.5)
            rotate(10deg);

        opacity: 1;
    }

    100% {
        transform:
            scale(1)
            rotate(0deg);

        opacity: 1;
    }

}

.result-box {

    text-align: center;

    background:
        rgba(255,255,255,0.10);

    border-radius: 20px;

    padding: 22px;

    margin-top: 18px;
}

.result-title {

    color: white;

    font-size: 32px;

    font-weight: 900;
}

.result-detail {

    color: #e5edff;

    font-size: 19px;
}

.final-title {

    text-align: center;

    color: white;

    font-size: 48px;

    font-weight: 900;

    text-shadow:
        0 0 15px #00eaff,
        0 0 30px #7b2cff;
}

.footer {

    text-align: center;

    color: #aebbd5;

    margin-top: 28px;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# GAME FUNCTIONS
# ============================================================

def determine_winner(
    user,
    computer
):

    if user == computer:
        return "tie"

    if (
        user == "rock"
        and computer == "scissor"
    ):
        return "user"

    if (
        user == "paper"
        and computer == "rock"
    ):
        return "user"

    if (
        user == "scissor"
        and computer == "paper"
    ):
        return "user"

    return "computer"


def reset_game():

    st.session_state.started = False

    st.session_state.round = 1

    st.session_state.user_wins = 0

    st.session_state.computer_wins = 0

    st.session_state.ties = 0

    st.session_state.user_choice = None

    st.session_state.computer_choice = None

    st.session_state.battle_started = False

    st.session_state.game_over = False


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.started:

    st.markdown(
        '<div class="main-title">'
        '🎮 Aditya\'s Games World 🎮'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'The ultimate Rock Paper Scissors battle!'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
### 🕹️ How to Play

- 🪨 Rock beats ✂️ Scissor
- 📄 Paper beats 🪨 Rock
- ✂️ Scissor beats 📄 Paper
- 🤝 Same weapon = Draw
- 🏆 Highest score after 10 rounds wins!

### 🎻 Game Atmosphere

Enter the game and a cinematic violin melody
will play in the background.

Every battle ends with a powerful
sniper-style game sound effect.
"""
    )

    if st.button(
        "🚀 ENTER THE GAME",
        use_container_width=True
    ):

        st.session_state.started = True

        st.rerun()

    st.markdown(
        '<div class="footer">'
        'Made with Python 🐍 + Streamlit ❤️'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# GAME
# ============================================================

elif not st.session_state.game_over:

    # --------------------------------------------------------
    # VIOLIN BACKGROUND MUSIC
    # --------------------------------------------------------

    st.markdown(
        '<audio autoplay loop style="display:none">'
        '<source src="data:audio/wav;base64,'
        + VIOLIN_BASE64
        + '" type="audio/wav">'
        '</audio>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    st.markdown(
        '<div class="main-title">'
        '🎮 ADITY\'S GAMES WORLD 🎮'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            '<div class="score-box">'
            '😎 YOU<br>'
            '<span class="score-number">'
            + str(st.session_state.user_wins)
            + '</span>'
            '</div>',
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            '<div class="score-box">'
            '🤖 COMPUTER<br>'
            '<span class="score-number">'
            + str(
                st.session_state.computer_wins
            )
            + '</span>'
            '</div>',
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            '<div class="score-box">'
            '🤝 DRAWS<br>'
            '<span class="score-number">'
            + str(st.session_state.ties)
            + '</span>'
            '</div>',
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # ROUND
    # --------------------------------------------------------

    st.markdown(
        '<div class="round-text">'
        'ROUND '
        + str(st.session_state.round)
        + ' / '
        + str(TOTAL_ROUNDS)
        + '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # CHOOSE WEAPON
    # ========================================================

    if not st.session_state.battle_started:

        st.markdown(
            '<div style="text-align:center;'
            'font-size:26px;'
            'font-weight:900;'
            'color:white;'
            'margin-bottom:18px;">'
            '⚔️ CHOOSE YOUR WEAPON ⚔️'
            '</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            if st.button(
                "🪨 ROCK",
                key="rock_button"
            ):

                st.session_state.user_choice = "rock"

                st.session_state.computer_choice = random.choice(
                    list(WEAPONS.keys())
                )

                st.session_state.battle_started = True

                st.rerun()


        with c2:

            if st.button(
                "📄 PAPER",
                key="paper_button"
            ):

                st.session_state.user_choice = "paper"

                st.session_state.computer_choice = random.choice(
                    list(WEAPONS.keys())
                )

                st.session_state.battle_started = True

                st.rerun()


        with c3:

            if st.button(
                "✂️ SCISSOR",
                key="scissor_button"
            ):

                st.session_state.user_choice = "scissor"

                st.session_state.computer_choice = random.choice(
                    list(WEAPONS.keys())
                )

                st.session_state.battle_started = True

                st.rerun()


    # ========================================================
    # BATTLE
    # ========================================================

    else:

        st.markdown(
            """
<div class="battle-box">

    <div class="fighter-name">
        😎 YOU
    </div>

    <div class="hand shake">
        🤜
    </div>

    <div style="
        font-size:30px;
        font-weight:900;
        color:white;
    ">
        VS
    </div>

    <div class="fighter-name">
        🤖 COMPUTER
    </div>

    <div class="hand shake">
        🤛
    </div>

</div>
""",
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # COUNTDOWN
        # ----------------------------------------------------

        st.markdown(
            '<div class="ready">'
            'READY?'
            '</div>',
            unsafe_allow_html=True
        )

        time.sleep(0.5)

        countdown = st.empty()

        for number in [3, 2, 1]:

            countdown.markdown(
                '<div style="'
                'text-align:center;'
                'font-size:75px;'
                'font-weight:900;'
                'color:white;">'
                + str(number)
                + '</div>',
                unsafe_allow_html=True
            )

            time.sleep(0.65)

        countdown.empty()


        # ----------------------------------------------------
        # SHOOT
        # ----------------------------------------------------

        st.markdown(
            '<div class="shoot">'
            '💥 SHOOT!'
            '</div>',
            unsafe_allow_html=True
        )

        time.sleep(0.15)

        st.markdown(
            '<div class="explosion">'
            '💥'
            '</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # SNIPER SOUND
        # ----------------------------------------------------

        st.audio(
            SNIPER,
            format="audio/wav",
            autoplay=True
        )

        time.sleep(0.45)


        # ----------------------------------------------------
        # REVEAL WEAPONS
        # ----------------------------------------------------

        user_weapon = WEAPONS[
            st.session_state.user_choice
        ]

        computer_weapon = WEAPONS[
            st.session_state.computer_choice
        ]

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown(
                '<div style="'
                'text-align:center;'
                'font-size:70px;">'
                + user_weapon
                + '</div>'
                '<div style="'
                'text-align:center;'
                'color:white;'
                'font-weight:900;">'
                'YOU'
                '</div>',
                unsafe_allow_html=True
            )


        with c2:

            st.markdown(
                '<div style="'
                'text-align:center;'
                'font-size:32px;'
                'font-weight:900;'
                'color:white;'
                'margin-top:25px;">'
                'VS'
                '</div>',
                unsafe_allow_html=True
            )


        with c3:

            st.markdown(
                '<div style="'
                'text-align:center;'
                'font-size:70px;">'
                + computer_weapon
                + '</div>'
                '<div style="'
                'text-align:center;'
                'color:white;'
                'font-weight:900;">'
                'COMPUTER'
                '</div>',
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        result = determine_winner(
            st.session_state.user_choice,
            st.session_state.computer_choice
        )


        if result == "user":

            st.session_state.user_wins += 1

            title = "🎉 YOU WIN!"

            detail = (
                "🔥 Excellent shot! "
                "You destroyed the computer!"
            )


        elif result == "computer":

            st.session_state.computer_wins += 1

            title = "🤖 COMPUTER WINS!"

            detail = (
                "💀 The computer got you "
                "this time!"
            )


        else:

            st.session_state.ties += 1

            title = "🤝 IT'S A DRAW!"

            detail = (
                "😐 Nobody wins this round!"
            )


        st.markdown(
            '<div class="result-box">'
            '<div class="result-title">'
            + title
            + '</div>'
            '<div class="result-detail">'
            + detail
            + '</div>'
            '</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # NEXT ROUND
        # ----------------------------------------------------

        if st.session_state.round < TOTAL_ROUNDS:

            if st.button(
                "➡️ NEXT ROUND",
                use_container_width=True
            ):

                st.session_state.round += 1

                st.session_state.user_choice = None

                st.session_state.computer_choice = None

                st.session_state.battle_started = False

                st.rerun()


        else:

            if st.button(
                "🏆 SEE FINAL SCORE",
                use_container_width=True
            ):

                st.session_state.game_over = True

                st.rerun()


# ============================================================
# FINAL SCORE
# ============================================================

else:

    st.balloons()

    st.markdown(
        '<div class="final-title">'
        '🏆 GAME OVER 🏆'
        '</div>',
        unsafe_allow_html=True
    )

    user_score = st.session_state.user_wins

    computer_score = (
        st.session_state.computer_wins
    )

    draws = st.session_state.ties


    if user_score > computer_score:

        title = "👑 YOU ARE THE CHAMPION!"

        message = (
            "🔥 Absolute domination! "
            "The computer has been destroyed!"
        )


    elif computer_score > user_score:

        title = "🤖 THE COMPUTER WINS!"

        message = (
            "💀 The machines have taken over... "
            "Revenge time!"
        )


    else:

        title = "🤝 PERFECTLY EVEN!"

        message = (
            "😎 Neither side could defeat "
            "the other!"
        )


    st.markdown(
        '<div class="result-box">'
        '<div class="result-title">'
        + title
        + '</div>'
        '<div class="result-detail">'
        + message
        + '</div>'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # FINAL SCORES
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            '<div class="result-box">'
            '😎<br>'
            'YOU<br>'
            '<b>'
            + str(user_score)
            + '</b>'
            '</div>',
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            '<div class="result-box">'
            '🤖<br>'
            'COMPUTER<br>'
            '<b>'
            + str(computer_score)
            + '</b>'
            '</div>',
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            '<div class="result-box">'
            '🤝<br>'
            'DRAWS<br>'
            '<b>'
            + str(draws)
            + '</b>'
            '</div>',
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # PLAY AGAIN
    # --------------------------------------------------------

    if st.button(
        "🔄 PLAY AGAIN",
        use_container_width=True
    ):

        reset_game()

        st.rerun()


    st.markdown(
        '<div class="footer">'
        '🎮 Thanks for playing '
        'Aditya\'s Games World!'
        '</div>',
        unsafe_allow_html=True
    )