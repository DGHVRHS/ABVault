
import streamlit as st
import math
import re
import ast
import operator

st.set_page_config(page_title="Unlock the Vault: Related Rates", layout="wide")

# Safe math parser supporting integers, fractions, decimals, and pi expressions (e.g., 60pi, -3/2, 188.5)
_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def parse_math_answer(raw_text):
    if not raw_text or not raw_text.strip():
        return None
    expr = raw_text.strip().lower().replace("π", "pi").replace("^", "**")
    # Convert implicit multiplication like "60pi" or "60 pi" into "60*pi"
    expr = re.sub(r"(\d)\s*(pi)\b", r"\1*\2", expr)
    expr = re.sub(r"\)\s*\(", r")*(", expr)
    expr = re.sub(r"\)\s*(pi|\d)", r")*\1", expr)

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name) and node.id == "pi":
            return math.pi
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
            return _ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
            return _ALLOWED_OPS[type(node.op)](_eval(node.operand))
        raise ValueError("Unsupported expression")

    try:
        tree = ast.parse(expr, mode="eval")
        val = _eval(tree)
        if math.isnan(val) or math.isinf(val):
            return None
        return float(val)
    except Exception:
        return None


# 3 Distinct Versions (6 Related Rates Locks per Version -> 6-Digit Vault Passcode)
VAULT_VERSIONS = {
    "Team 1 — Alpha Vault": {
        "color": "🔵",
        "passcode": ["4", "8", "2", "9", "1", "6"],
        "locks": [
            {
                "title": "Lock 1: The Sliding Ladder",
                "problem": (
                    r"A $10\text{-foot}$ ladder is leaning against a vertical wall. If the bottom of the ladder is pulled "
                    r"away from the wall along level ground at a constant rate of $4\text{ ft/s}$, find $\frac{dy}{dt}$ "
                    r"(in $\text{ft/s}$), the rate at which the height $y$ of the top of the ladder is changing at the "
                    r"instant when the bottom of the ladder is $6\text{ feet}$ from the wall."
                ),
                "formula": r"$x^2 + y^2 = z^2$",
                "answer_val": -3.0,
                "answer_disp": r"$-3\text{ ft/s}$"
            },
            {
                "title": "Lock 2: Particle on an Implicit Curve",
                "problem": (
                    r"A particle moves along the curve defined by $x^2 + xy + y^2 = 7$, where $x$ and $y$ are differentiable "
                    r"functions of $t$ (in seconds). At the instant the particle passes through the point $(2, 1)$, its "
                    r"$x$-coordinate is decreasing at a rate of $2\text{ units/s}$ ($\frac{dx}{dt} = -2$). Find $\frac{dy}{dt}$ at that instant."
                ),
                "formula": r"Product Rule: $\frac{d}{dt}(xy) = x\frac{dy}{dt} + y\frac{dx}{dt}$",
                "answer_val": 2.5,
                "answer_disp": r"$\frac{5}{2}$ or $2.5\text{ units/s}$"
            },
            {
                "title": "Lock 3: Expanding Circular Spill",
                "problem": (
                    r"Oil spills from a ruptured tanker and spreads in a circular pattern. If the radius of the spill "
                    r"increases at a constant rate of $2\text{ m/s}$, how fast is the area $A$ of the spill increasing "
                    r"(in $\text{m}^2/\text{s}$) when the radius is $15\text{ m}$?"
                ),
                "formula": r"$A = \pi r^2$",
                "answer_val": 60.0 * math.pi,
                "answer_disp": r"$60\pi\text{ m}^2/\text{s}$ ($\approx 188.50$)"
            },
            {
                "title": "Lock 4: Expanding Cube",
                "problem": (
                    r"Each edge $s$ of a metal cube is expanding at a constant rate of $2\text{ cm/s}$. How fast is the "
                    r"volume $V$ of the cube increasing (in $\text{cm}^3/\text{s}$) at the instant when the volume is $64\text{ cm}^3$?"
                ),
                "formula": r"$V = s^3$",
                "answer_val": 96.0,
                "answer_disp": r"$96\text{ cm}^3/\text{s}$"
            },
            {
                "title": "Lock 5: Cylindrical Water Tank",
                "problem": (
                    r"A vertical cylindrical tank with a fixed radius of $4\text{ m}$ is being filled with water at a "
                    r"constant rate of $32\pi\text{ m}^3/\text{min}$. How fast is the height $h$ of the water increasing "
                    r"(in $\text{m/min}$)?"
                ),
                "formula": r"$V = \pi r^2 h$",
                "answer_val": 2.0,
                "answer_disp": r"$2\text{ m/min}$"
            },
            {
                "title": "Lock 6: Spherical Balloon (Final Lock)",
                "problem": (
                    r"A spherical weather balloon is inflated so that its surface area $S$ increases at a constant rate of "
                    r"$24\pi\text{ cm}^2/\text{s}$. How fast is the volume $V$ increasing (in $\text{cm}^3/\text{s}$) at "
                    r"the instant when the surface area is $100\pi\text{ cm}^2$?"
                ),
                "formula": r"$S = 4\pi r^2$ and $V = \frac{4}{3}\pi r^3$",
                "answer_val": 60.0 * math.pi,
                "answer_disp": r"$60\pi\text{ cm}^3/\text{s}$ ($\approx 188.50$)"
            }
        ]
    },
    "Team 2 — Bravo Vault": {
        "color": "🔴",
        "passcode": ["7", "3", "9", "5", "2", "8"],
        "locks": [
            {
                "title": "Lock 1: The Sliding Ladder",
                "problem": (
                    r"A $15\text{-foot}$ ladder is leaning against a vertical wall. If the bottom of the ladder is pulled "
                    r"away from the wall along level ground at a constant rate of $2\text{ ft/s}$, find $\frac{dy}{dt}$ "
                    r"(in $\text{ft/s}$), the rate at which the height $y$ of the top of the ladder is changing at the "
                    r"instant when the bottom of the ladder is $9\text{ feet}$ from the wall."
                ),
                "formula": r"$x^2 + y^2 = z^2$",
                "answer_val": -1.5,
                "answer_disp": r"$-\frac{3}{2}$ or $-1.5\text{ ft/s}$"
            },
            {
                "title": "Lock 2: Particle on an Implicit Curve",
                "problem": (
                    r"A particle moves along the curve defined by $x^3 + xy - y^2 = 8$, where $x$ and $y$ are differentiable "
                    r"functions of $t$ (in seconds). At the instant the particle passes through the point $(2, 2)$, its "
                    r"$x$-coordinate is increasing at a rate of $1\text{ unit/s}$ ($\frac{dx}{dt} = 1$). Find $\frac{dy}{dt}$ at that instant."
                ),
                "formula": r"Product Rule: $\frac{d}{dt}(xy) = x\frac{dy}{dt} + y\frac{dx}{dt}$",
                "answer_val": 7.0,
                "answer_disp": r"$7\text{ units/s}$"
            },
            {
                "title": "Lock 3: Circular Water Ripple",
                "problem": (
                    r"A stone dropped into a calm pond creates a circular ripple whose radius increases at a constant rate "
                    r"of $3\text{ cm/s}$. How fast is the area $A$ enclosed by the ripple increasing (in $\text{cm}^2/\text{s}$) "
                    r"when the radius is $8\text{ cm}$?"
                ),
                "formula": r"$A = \pi r^2$",
                "answer_val": 48.0 * math.pi,
                "answer_disp": r"$48\pi\text{ cm}^2/\text{s}$ ($\approx 150.80$)"
            },
            {
                "title": "Lock 4: Morphing Rectangle",
                "problem": (
                    r"The length $l$ of a rectangle is increasing at a rate of $5\text{ cm/s}$ while its width $w$ is "
                    r"decreasing at a rate of $2\text{ cm/s}$ ($\frac{dw}{dt} = -2$). How fast is the area $A$ of the rectangle "
                    r"changing (in $\text{cm}^2/\text{s}$) when $l = 12\text{ cm}$ and $w = 10\text{ cm}$?"
                ),
                "formula": r"$A = l \cdot w$",
                "answer_val": 26.0,
                "answer_disp": r"$26\text{ cm}^2/\text{s}$"
            },
            {
                "title": "Lock 5: Draining Cylindrical Drum",
                "problem": (
                    r"Oil is draining from a vertical cylindrical drum with a fixed radius of $3\text{ ft}$ at a rate of "
                    r"$18\pi\text{ ft}^3/\text{min}$ ($\frac{dV}{dt} = -18\pi$). Find $\frac{dh}{dt}$ (in $\text{ft/min}$), "
                    r"the rate at which the height $h$ of the oil is changing."
                ),
                "formula": r"$V = \pi r^2 h$",
                "answer_val": -2.0,
                "answer_disp": r"$-2\text{ ft/min}$"
            },
            {
                "title": "Lock 6: Spherical Balloon (Final Lock)",
                "problem": (
                    r"A spherical balloon is inflated so that its surface area $S$ increases at a constant rate of "
                    r"$12\pi\text{ cm}^2/\text{s}$. How fast is the volume $V$ increasing (in $\text{cm}^3/\text{s}$) at "
                    r"the instant when the surface area is $64\pi\text{ cm}^2$?"
                ),
                "formula": r"$S = 4\pi r^2$ and $V = \frac{4}{3}\pi r^3$",
                "answer_val": 24.0 * math.pi,
                "answer_disp": r"$24\pi\text{ cm}^3/\text{s}$ ($\approx 75.40$)"
            }
        ]
    },
    "Team 3 — Charlie Vault": {
        "color": "🟢",
        "passcode": ["6", "1", "5", "8", "4", "3"],
        "locks": [
            {
                "title": "Lock 1: The Sliding Ladder",
                "problem": (
                    r"A $25\text{-foot}$ ladder is leaning against a vertical wall. If the bottom of the ladder is pulled "
                    r"away from the wall along level ground at a constant rate of $6\text{ ft/s}$, find $\frac{dy}{dt}$ "
                    r"(in $\text{ft/s}$), the rate at which the height $y$ of the top of the ladder is changing at the "
                    r"instant when the bottom of the ladder is $7\text{ feet}$ from the wall."
                ),
                "formula": r"$x^2 + y^2 = z^2$",
                "answer_val": -1.75,
                "answer_disp": r"$-\frac{7}{4}$ or $-1.75\text{ ft/s}$"
            },
            {
                "title": "Lock 2: Particle on an Implicit Curve",
                "problem": (
                    r"A particle moves along the curve defined by $2x^2 - xy + y^3 = 7$, where $x$ and $y$ are differentiable "
                    r"functions of $t$ (in seconds). At the instant the particle passes through the point $(2, 1)$, its "
                    r"$x$-coordinate is decreasing at a rate of $2\text{ units/s}$ ($\frac{dx}{dt} = -2$). Find $\frac{dy}{dt}$ at that instant."
                ),
                "formula": r"Product Rule: $\frac{d}{dt}(xy) = x\frac{dy}{dt} + y\frac{dx}{dt}$",
                "answer_val": 14.0,
                "answer_disp": r"$14\text{ units/s}$"
            },
            {
                "title": "Lock 3: Expanding Metal Disc",
                "problem": (
                    r"When heated, a circular metal plate expands so that its radius increases at a constant rate of "
                    r"$0.5\text{ mm/s}$. How fast is the area $A$ of the plate increasing (in $\text{mm}^2/\text{s}$) "
                    r"when the radius is $20\text{ mm}$?"
                ),
                "formula": r"$A = \pi r^2$",
                "answer_val": 20.0 * math.pi,
                "answer_disp": r"$20\pi\text{ mm}^2/\text{s}$ ($\approx 62.83$)"
            },
            {
                "title": "Lock 4: Expanding Cube",
                "problem": (
                    r"Each edge $s$ of a cube is increasing at a constant rate of $3\text{ in/s}$. How fast is the "
                    r"volume $V$ of the cube increasing (in $\text{in}^3/\text{s}$) at the instant when the total surface "
                    r"area $S$ of the cube is $150\text{ in}^2$?"
                ),
                "formula": r"$V = s^3$ and $S = 6s^2$",
                "answer_val": 225.0,
                "answer_disp": r"$225\text{ in}^3/\text{s}$"
            },
            {
                "title": "Lock 5: Cylindrical Vat",
                "problem": (
                    r"Water is poured into a vertical cylindrical vat with a fixed radius of $6\text{ m}$ at a constant "
                    r"rate of $54\pi\text{ m}^3/\text{min}$. How fast is the height $h$ of the water rising "
                    r"(in $\text{m/min}$)?"
                ),
                "formula": r"$V = \pi r^2 h$",
                "answer_val": 1.5,
                "answer_disp": r"$\frac{3}{2}$ or $1.5\text{ m/min}$"
            },
            {
                "title": "Lock 6: Melting Snowball (Final Lock)",
                "problem": (
                    r"A spherical snowball melts so that its surface area $S$ decreases at a constant rate of "
                    r"$14\pi\text{ cm}^2/\text{min}$ ($\frac{dS}{dt} = -14\pi$). Find $\frac{dV}{dt}$ (in $\text{cm}^3/\text{min}$), "
                    r"the rate at which the volume $V$ is changing when the surface area is $196\pi\text{ cm}^2$."
                ),
                "formula": r"$S = 4\pi r^2$ and $V = \frac{4}{3}\pi r^3$",
                "answer_val": -49.0 * math.pi,
                "answer_disp": r"$-49\pi\text{ cm}^3/\text{min}$ ($\approx -153.94$)"
            }
        ]
    }
}

# --- SESSION STATE INITIALIZATION ---
if "solved_locks" not in st.session_state:
    st.session_state.solved_locks = {v: set() for v in VAULT_VERSIONS}
if "vault_opened" not in st.session_state:
    st.session_state.vault_opened = {v: False for v in VAULT_VERSIONS}

# --- HEADER & VERSION SELECTOR ---
st.title("🔐 Unlock the Vault: Related Rates Race")
st.markdown(
    "Solve all **6 Related Rates problems** to reveal the **6 digits** of your team's vault passcode. "
    "Enter the complete 6-digit combination at the bottom to crack open your vault first!"
)

sel_col, name_col, reset_col = st.columns([1.5, 1.5, 0.8])
with sel_col:
    selected_version = st.selectbox("Select Your Team's Vault Version:", list(VAULT_VERSIONS.keys()))
with name_col:
    team_members = st.text_input("Team Members:", placeholder="Enter your names")
with reset_col:
    st.write("")
    st.write("")
    if st.button("🔄 Reset This Vault", use_container_width=True):
        st.session_state.solved_locks[selected_version] = set()
        st.session_state.vault_opened[selected_version] = False
        st.rerun()

v_data = VAULT_VERSIONS[selected_version]
solved_set = st.session_state.solved_locks[selected_version]
passcode_digits = v_data["passcode"]

# --- LIVE PASSCODE TRACKER DISPLAY ---
st.divider()
st.subheader(f"{v_data['color']} {selected_version} — Collected Passcode Digits ({len(solved_set)} / 6)")

digit_cols = st.columns(6)
for idx in range(6):
    with digit_cols[idx]:
        with st.container(border=True):
            st.caption(f"Digit #{idx + 1}")
            if idx in solved_set:
                st.markdown(f"## 🔓 `{passcode_digits[idx]}`")
            else:
                st.markdown("## 🔒 `?`")

# --- 6 RELATED RATES CHALLENGES ---
st.divider()
st.header("Related Rates Security Locks")
st.caption("Tip: You can enter integers (`-3`), fractions (`-3/2`), exact pi terms (`60pi`), or decimals rounded to two places (`188.50`). Include negative signs when a quantity is decreasing!")

for idx, lock in enumerate(v_data["locks"]):
    is_solved = idx in solved_set
    status_icon = "✅ UNLOCKED" if is_solved else "🔒 LOCKED"

    with st.container(border=True):
        st.subheader(f"{lock['title']} — {status_icon}")
        st.markdown(lock["problem"])
        st.info(f"**Given Formula:** {lock['formula']}")

        if is_solved:
            st.success(
                f"🎉 **Correct!** Answer: {lock['answer_disp']}  |  "
                f"**Vault Digit #{idx + 1} Revealed:** **`{passcode_digits[idx]}`**"
            )
        else:
            in_col, btn_col = st.columns([3, 1])
            with in_col:
                user_raw = st.text_input(
                    f"Enter your answer for Lock {idx + 1}:",
                    key=f"input_{selected_version}_{idx}",
                    placeholder="e.g., -3, 2.5, or 60pi"
                )
            with btn_col:
                st.write("")
                st.write("")
                check_clicked = st.button("Check Answer", key=f"btn_{selected_version}_{idx}", use_container_width=True)

            if check_clicked:
                parsed = parse_math_answer(user_raw)
                if parsed is None:
                    st.error("⚠️ Please enter a valid number, fraction, or $\pi$ expression (such as `60pi` or `-3/2`).")
                elif abs(parsed - lock["answer_val"]) <= 0.05:
                    st.session_state.solved_locks[selected_version].add(idx)
                    st.rerun()
                else:
                    st.error("❌ Incorrect rate — check your implicit differentiation, signs, and units, then try again!")

# --- FINAL VAULT KEYPAD ---
st.divider()
st.header("🏦 Final Vault Keypad")

full_code = "".join(passcode_digits)

if st.session_state.vault_opened[selected_version]:
    st.balloons()
    who = team_members.strip() if team_members.strip() else selected_version
    st.success(
        f"🏆 **VAULT UNLOCKED!** Congratulations **{who}**! You cracked **{selected_version}** "
        f"with passcode **`{full_code}`**! Raise your hand to claim victory!"
    )
else:
    if len(solved_set) < 6:
        st.info(f"Solve all 6 locks above to reveal every digit of your passcode ({6 - len(solved_set)} remaining).")

    k_col1, k_col2 = st.columns([2, 1])
    with k_col1:
        code_attempt = st.text_input(
            "Enter the 6-Digit Vault Passcode:",
            max_chars=6,
            placeholder="######",
            key=f"keypad_{selected_version}"
        )
    with k_col2:
        st.write("")
        st.write("")
        if st.button("🔓 UNLOCK VAULT", type="primary", use_container_width=True):
            if code_attempt.strip() == full_code:
                st.session_state.vault_opened[selected_version] = True
                st.rerun()
            else:
                st.error("🚨 **ACCESS DENIED!** Incorrect 6-digit passcode.")
