import streamlit as st
import csv
import random
import io
import textwrap

# ---------------------------------------------------------
# 🔐 [1] 수강생 관리 (아이디와 비번 설정)
# ---------------------------------------------------------
USERS = {
    "student01": "tarot123",
    "vip": "love2025",
    "admin": "masterkey"
}

# ---------------------------------------------------------
# 💾 [2] 데이터베이스 (현실적 문제 5종 포함)
# ---------------------------------------------------------
csv_data = """ID,Type,Group,Title,Logic,Description
T01,Timing,초고속,1시간 이내,Do < 1 deg + Cardinal + Angle,상황이 매우 급박합니다. 지금 당장 혹은 1시간 이내에 소식이 옵니다.
T02,Timing,초고속,3시간 이내,Do 1-3 deg + Cardinal + Angle,오늘 반나절이 가기 전에 3시간 안쪽으로 연락이 닿습니다.
T03,Timing,초고속,12시간 이내,Moon enters Angle < 12h,오늘 밤이나 내일 아침 해가 뜨기 전까지 연락이 올 것입니다.
T04,Timing,초고속,24시간(1일) 이내,Do ~1 deg + Cardinal,내일 이 시간 전까지는 무조건 연락이 옵니다.
T05,Timing,초고속,2일 이내,Do 2 deg + Cardinal,이틀 안으로 결판이 납니다. 모레까지 기다려보세요.
T06,Timing,초고속,3일 이내,Do 3 deg + Cardinal,작심삼일이라 했습니다. 3일 안에 행동이 개시됩니다.
T07,Timing,초고속,4일 후,Do 4 deg + Cardinal,숫자 4가 뜹니다. 4일 뒤에 연락이 닿을 확률이 높습니다.
T08,Timing,빠름,1주일 이내,Do 5-7 deg + Cardinal,이번 주말이나 다음 주 초 늦어도 7일 안에는 연락이 옵니다.
T09,Timing,빠름,10일 이내,Do ~10 deg + Cardinal,열흘 정도의 시간이 걸립니다. 마음을 조금만 비우고 기다리세요.
T10,Timing,빠름,2주 후 (보름),Moon Cycle (15 deg),달이 차오를 때쯤 연락이 옵니다. 약 15일 정도 예상됩니다.
T11,Timing,빠름,3주 후,Do 3 deg + Fixed/Mutable,한 달을 넘기지는 않습니다. 3주 정도 뒤에 소식이 옵니다.
T12,Timing,빠름,4주(1개월) 이내,Moon Return (28 days),이번 달 안에는 연락이 옵니다. 한 달 정도의 텀이 있습니다.
T13,Timing,보통,1개월 후,Do 1 deg + Fixed (Month),계절이 살짝 바뀔 때쯤 다음 달 이맘때 연락이 옵니다.
T14,Timing,보통,6주 후,Do 6 deg + Mutable,한 달 반 정도의 시간이 필요합니다. 서로 생각할 시간이 필요해요.
T15,Timing,보통,2개월 후,Do 2 deg + Fixed,두 달 뒤에 연락이 옵니다. 조금 긴 호흡으로 기다려야 합니다.
T16,Timing,보통,3개월 후,Do 3 deg + Fixed,한 분기가 지나야 합니다. 가장 흔한 재회 텀인 3개월 뒤입니다.
T17,Timing,보통,4개월 후,Do 4 deg + Fixed,꽤 오래 기다려야 합니다. 4개월 뒤에야 기회가 생깁니다.
T18,Timing,보통,5개월 후,Do 5 deg + Fixed,잊을 만하면 연락이 옵니다. 5개월 정도 예상하세요.
T19,Timing,느림,6개월(반년) 후,Do 6 deg + Fixed,아주 오랜 시간이 걸립니다. 반년 뒤에나 기약할 수 있습니다.
T20,Timing,느림,1년 후,Solar Return,올해는 어렵습니다. 내년이나 되어야 인연이 닿습니다.
T21,Timing,미상,시기 미상,Planet Slow / Retrograde,행성의 속도가 너무 느려 언제인지 특정할 수 없습니다. 기약이 없습니다.
T22,Timing,지연,영구적 지연 (End),Saturn Interference,약속은 계속 깨지고 만남은 영원히 미뤄집니다. 사실상 끝입니다.
T23,Timing,특수,새벽/아침,Sun in 12H/1H,해가 뜨는 이른 아침 시간대에 연락이 올 것입니다.
T24,Timing,특수,점심/낮,Sun in 10H/9H,해가 중천에 뜬 점심 시간 혹은 낮 시간에 연락이 옵니다.
T25,Timing,특수,저녁/밤,Sun in 7H/6H,해가 질 무렵이나 저녁 식사 시간에 연락이 옵니다.
T26,Timing,특수,한밤중,Sun in 4H/3H,모두가 잠든 심야 시간에 감성적인 연락이 올 것입니다.
T27,Timing,특수,주말,Lord is Saturn/Sun,평일은 바쁘고 토요일이나 일요일 주말에 연락이 옵니다.
T28,Timing,특수,공휴일/기념일,Benefic Planet Day,빨간 날이나 생일 등 특별한 날에 연락이 닿습니다.
T29,Timing,특수,한가해질 때,Leaving Cadent House,상대가 바쁜 일이 끝나고 여유가 생겨야 연락이 옵니다.
T30,Timing,불가,타이밍 놓침,Separating Aspect > 3 deg,이미 기회는 지나갔습니다. 연락이 오기 어렵습니다.
S01,Situation,긍정,완벽한 합 (Conjunction),L1 conj L7 (Applying),장애물이 없는 완벽한 재회입니다. 서로 다시 만나 하나가 됩니다.|상대는 당신을 그리워하고 있으며 곧 행동을 취할 것입니다.|재회 성공 확률이 매우 높습니다.|장애물이 사라지고 두 사람의 마음이 하나로 합쳐지는 시기입니다.
S02,Situation,긍정,급발진 연락,Mars L7 in Angle,상대가 참지 못하고 충동적으로 연락합니다.|화성(Mars)의 영향으로 성격이 급해진 상태입니다.|갑작스러운 전화나 문자가 올 것입니다.|생각지도 못한 타이밍에 상대가 들이닥칠 수 있으니 마음의 준비를 하세요.
S03,Situation,긍정,염탐하다 실수,Mercury Rx / Combust,상대가 몰래 SNS를 보다가 실수로 흔적을 남깁니다.|자존심 때문에 연락은 못하고 염탐만 하고 있습니다.|실수를 계기로 대화가 시작될 수 있습니다.|상대의 귀여운 실수를 모른 척 받아주면 관계가 급진전됩니다.
S101,Situation,부정,업무 과부하 (Burnout),Mars in 6H (Work),일이 쓰나미처럼 몰려와서 잠잘 시간도 없는 상태입니다.|'바빠서 죽겠다'는 말이 빈말이 아닙니다. 육체적 정신적 에너지가 0에 가깝습니다.|당신이 싫은 게 아니라 생존을 위해 일만 해야 하는 시기입니다.|과로로 쓰러지기 직전인 사람에게 연애는 사치입니다.
S102,Situation,부정,금전적 위기 (Money Block),2H Malefic / South Node,심각한 자금난 빚 독촉 혹은 돈줄이 막혀버린 상황입니다.|경제적 능력을 상실하여 자존감이 바닥을 치고 있습니다.|'돈 없는 내가 무슨 연애냐'라는 자괴감에 빠져 있습니다.|금전 문제가 해결되기 전까지는 남자로 구실을 못한다고 생각하여 숨어있을 것입니다.
S103,Situation,부정,소송 및 관재구설 (Legal),7H Malefic (Dispute),누군가와 법적 분쟁 소송 혹은 심각한 계약 위반으로 싸우고 있습니다.|머릿속이 온통 '이 싸움에서 이기는 법'이나 '수습하는 법'으로 가득 차 있습니다.|연애 감정을 느낄 뇌의 용량이 남아있지 않습니다.|지금 연락하면 당신에게 화풀이를 하거나 귀찮아할 수 있습니다. 전쟁 중인 사람입니다.
S104,Situation,부정,사업/프로젝트 붕괴,10H Lord Retrograde,야심 차게 준비하던 사업이나 프로젝트가 엎어졌거나 큰 차질이 생겼습니다.|성공을 위해 달려왔는데 결과가 처참해 좌절하고 있습니다.|패배감에 젖어 아무도 만나고 싶어 하지 않는 '동굴 모드'입니다.|재기하기 위해 수습하느라 정신이 없습니다. 위로도 귀에 들어오지 않을 겁니다.
S105,Situation,부정,멘탈 붕괴 (Panic),Moon/Mercury Afflicted,극심한 스트레스로 인해 공황장애에 가까운 멘탈 붕괴가 왔습니다.|이성적인 사고가 불가능하며 감정 기복이 롤러코스터를 타고 있습니다.|누구와 대화할 수 있는 정신 상태가 아닙니다.|지금은 혼자 두는 것이 그를 도와주는 유일한 방법입니다. 치료가 필요해 보입니다.
S50,Situation,부정,끝난 인연,Separation > 6 deg,운명적으로 인연의 끈이 다했습니다.|이미 서로의 마음이 정리된 상태입니다.|되돌리기엔 너무 멀리 왔습니다.|아쉽지만 이제는 각자의 길을 가는 것이 서로를 위한 길입니다. 더 이상의 미련은 독입니다.
S54,Situation,중립,후회 중,Retrograde No Aspect,헤어진 걸 후회하지만 용기가 없어 다가오지 못합니다.|자존심과 미련 사이에서 갈팡질팡하고 있습니다.|먼저 다가가면 받아줄 가능성이 있습니다.|상대는 당신이 먼저 손 내밀어 주기를 기다리고 있을지도 모릅니다.
S90,Situation,부정,현실의 벽 (My Marriage),L1 Besieged / Prohibition,당신은 이미 결혼을 했거나 짝이 있는 상태입니다.|현재 당신의 상황이 이 관계를 허락하지 않습니다.|마음 한구석에 미련은 있지만 현실적으로 불가능함을 당신도 알고 있습니다.|지금의 가정을 지키는 것이 운명의 순리입니다. 과거는 과거로 남겨두세요.
S91,Situation,부정,오래된 단절,Separation > 1 Year,서로 보지 못한 지 너무나 오랜 시간이 흘렀습니다.|이미 두 사람의 인연의 끈은 1년 전 그 시점에 끊어졌습니다.|상대방의 기억 속에서 당신은 점점 희미해져 가고 있습니다.|죽은 나무에 물을 주어도 꽃은 피지 않습니다. 이제는 놓아주어야 할 때입니다.
S92,Situation,중립,스쳐가는 바람,Weak Aspect / Past,가끔 생각나고 아주 가끔 연락은 닿았지만 그뿐입니다.|인연이 이어질 듯 말 듯 했지만 결국 타이밍을 놓쳤습니다.|상대도 당신을 '한때 알았던 사람' 정도로만 생각하고 있습니다.|재회보다는 가끔 안부나 묻는 먼 지인으로 남는 것이 최선입니다.
"""

# ---------------------------------------------------------
# 🤖 [3] 호라리 엔진
# ---------------------------------------------------------
class HoraryBot:
    def __init__(self, raw_csv):
        self.situations = {'긍정': [], '부정': [], '중립': []}
        self.timings = {'초고속': [], '빠름': [], '보통': [], '느림': [], '미상': [], '지연': [], '특수': [], '불가': []}
        
        f = io.StringIO(raw_csv.strip())
        reader = csv.DictReader(f)
        for row in reader:
            if row['Type'] == 'Situation':
                parts = row['Description'].split('|')
                if len(parts) >= 4:
                    row['Detail_Situation'] = parts[0]
                    row['Detail_Psychology'] = parts[1]
                    row['Detail_Conclusion'] = parts[2]
                    row['Detail_Summary'] = parts[3]
                else:
                    row['Detail_Situation'] = row['Description']
                    row['Detail_Psychology'] = "추가 정보 없음"
                    row['Detail_Conclusion'] = "분석 중"
                    row['Detail_Summary'] = row['Description']
                
                self.situations[row['Group']].append(row)
            elif row['Type'] == 'Timing':
                self.timings[row['Group']].append(row)

    def draw_card(self):
        # 확률 로직
        fate_roll = random.random()
        if fate_roll < 0.35: 
            outcome = '긍정'
            s_card = random.choice(self.situations['긍정'])
            t_pool = self.timings['초고속'] + self.timings['빠름'] + self.timings['보통'] + self.timings['특수']
            t_card = random.choice(t_pool)
        elif fate_roll < 0.75:
            outcome = '부정'
            s_card = random.choice(self.situations['부정'])
            t_pool = self.timings['미상'] + self.timings['불가'] + self.timings['지연']
            t_card = random.choice(t_pool)
        else:
            outcome = '중립'
            s_card = random.choice(self.situations['중립'])
            t_pool = self.timings['보통'] + self.timings['느림'] + self.timings['지연'] + self.timings['특수']
            t_card = random.choice(t_pool)

        return s_card, t_card, outcome

# ---------------------------------------------------------
# 🖥️ [4] 메인 화면 및 로그인 로직 (수정된 부분)
# ---------------------------------------------------------
def check_password():
    """로그인 확인 함수"""
    def password_entered():
        if st.session_state["username"] in USERS and \
           st.session_state["password"] == USERS[st.session_state["username"]]:
            st.session_state["password_correct"] = True
            # [수정] 로그인 성공 시 아이디를 별도로 저장 (오류 방지)
            st.session_state["logged_in_user"] = st.session_state["username"] 
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.header("🔒 수강생 전용 호라리 타로")
        st.text_input("아이디(ID)", key="username")
        st.text_input("비밀번호(PW)", type="password", key="password")
        st.button("로그인", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        st.header("🔒 수강생 전용 호라리 타로")
        st.text_input("아이디(ID)", key="username")
        st.text_input("비밀번호(PW)", type="password", key="password")
        st.button("로그인", on_click=password_entered)
        st.error("😕 아이디 또는 비밀번호가 틀렸습니다.")
        return False
    else:
        return True

def main():
    st.set_page_config(page_title="신비의 호라리 타로", page_icon="🔮")

    if check_password():
        st.title("🔮 AI 호라리 타로 상담소")
        # [수정] 저장된 아이디를 불러오도록 변경
        st.caption(f"환영합니다, {st.session_state.get('logged_in_user', '방문자')}님! 당신의 고민을 들려주세요.")
        st.divider()

        if 'bot' not in st.session_state:
            st.session_state['bot'] = HoraryBot(csv_data)

        with st.form("question_form"):
            user_question = st.text_area("질문을 입력하세요", height=80, placeholder="예: 그 사람에게 연락이 올까요?")
            submitted = st.form_submit_button("타로 카드 뽑기 🎴")

            if submitted and user_question:
                with st.spinner('별들의 움직임을 계산하고 있습니다...'):
                    s_card, t_card, outcome = st.session_state['bot'].draw_card()
                    st.success("카드가 선택되었습니다!")
                    with st.container():
                        st.subheader(f"🎴 {s_card['Title']}")
                        st.caption(f"Logic: {s_card['Logic']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"**📍 상황**\n\n{s_card['Detail_Situation']}")
                        with col2:
                            st.warning(f"**🧠 심리**\n\n{s_card['Detail_Psychology']}")
                        st.error(f"**⚖️ 결론**\n\n{s_card['Detail_Conclusion']}")
                        st.markdown("---")
                        st.markdown(f"### 📝 요약 조언")
                        st.write(s_card['Detail_Summary'])
                        st.markdown("---")
                        if outcome == '부정' and '이내' in t_card['Title']:
                            st.write(f"🕒 **예상 시기:** {t_card['Title']} (단, 문제가 해결되어야 함)")
                        else:
                            st.write(f"🕒 **예상 시기:** {t_card['Title']}")
                        st.caption(f"시기 원리: {t_card['Logic']}")

if __name__ == "__main__":
    main()
